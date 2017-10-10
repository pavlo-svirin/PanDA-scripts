#!/usr/bin/env python

# This script is for running LQCD test jobs through PanDA
#

import sys
import time
import commands
import json

import userinterface.Client as Client
from taskbuffer.JobSpec import JobSpec
from taskbuffer.FileSpec import FileSpec

aSrvID = None

for idx,argv in enumerate(sys.argv):
    if argv == '-s':
        aSrvID = sys.argv[idx+1]
        sys.argv = sys.argv[:idx]
        break

site = 'ANALY_ORNL_Titan_LQCD'

datasetName = 'panda.destDB.%s' % commands.getoutput('uuidgen')
destName    = 'local'

job = JobSpec()
job.jobDefinitionID   = int(time.time()) % 10000
job.jobName           = "%s" % commands.getoutput('uuidgen')
# MPI transform on Titan that will run actual job
job.transformation    = '#json#'

job.destinationDBlock = datasetName
job.destinationSE     = destName
job.currentPriority   = 1000
job.prodSourceLabel   = 'user'
job.computingSite     = site

lqcd_command = {
		"nodes" : 7983,
		"walltime" : "20:00:00",
		"name" : "nt12b6680",
		"command" : """
export PMI_NO_FORK=1
export CRAY_CUDA_MPS=1

cd $PBS_O_WORKDIR
date

for i in {0..12}
do
aprun -n 168 -N 1 ./wrapper2_list.sh $((i*168)) &
sleep 1s
done
aprun -n 157 -N 1 ./wrapper2_list.sh 2184 &
sleep 1s

for i in {0..32}
do
aprun -n 168 -N 1 ./wrapper2.sh $((i*168+5200)) &
sleep 1s
done
aprun -n 98 -N 1 ./wrapper2.sh 10744
"""
		}

job.jobParameters = json.dumps(lqcd_command)

fileOL = FileSpec()
fileOL.lfn = "%s.job.log.tgz" % job.jobName
fileOL.destinationDBlock = job.destinationDBlock
fileOL.destinationSE     = job.destinationSE
fileOL.dataset           = job.destinationDBlock
fileOL.type = 'log'
job.addFile(fileOL)


for i in range(1):
	s,o = Client.submitJobs([job],srvID=aSrvID)
	print s
	print o
	for x in o:
		print "PandaID=%s" % x[0]
