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

site = 'ANALY_NERSC_LSST'

datasetName = 'panda.destDB.%s' % commands.getoutput('uuidgen')
destName    = 'local'

job = JobSpec()
job.jobDefinitionID   = int(time.time()) % 10000
job.jobName           = "%s" % commands.getoutput('uuidgen')
# MPI transform on Titan that will run actual job
job.transformation    = '#json#'
job.prodDBlock = "input.dataset"

fileD = FileSpec()
#fileD.dataset    = 'gfal.tgz'
#fileD.prodDBlock = fileD.dataset
fileD.lfn = 'gfal.tgz'
fileD.scope=""
fileD.type = 'input'
fileD.GUID = 'GO-test'
fileD.prodDBlock = job.prodDBlock
fileD.dataset = job.prodDBlock
fileD.status = 'ready'
job.addFile(fileD)

job.destinationDBlock = datasetName
job.destinationSE     = destName
job.currentPriority   = 1000
job.prodSourceLabel   = 'user'
job.VO = "lqcd"
job.metadata = ''
job.computingSite     = site
job.cmtConfig = json.dumps({'name' : 'BBBB', 'next' : None})

lqcd_command = {
		"nodes" : 1,
		"walltime" : "00:02:00",
		"name" : "lqcd-test",
		"next" : None,
		"command" : """
srun -n 4 shifter /home/lss/CoLoRe/runCoLoRe /input/param.cfg

echo "-----------------------------------------------------"
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
