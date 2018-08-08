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

site = 'ANALY_BNL_IC_LQCD'

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
job.VO = "lqcd"
job.metadata = ''
job.computingSite     = site
job.cmtConfig = json.dumps({'name' : 'IC-Test', 'next' : None})


lqcd_command = {
		"nodes" : 1,
		"walltime" : "15:00:00",
		"name" : "lqcd-test",
		"next" : None,
		"command" : """
#! /bin/bash

#SBATCH -p long
#SBATCH --time=15:00:00
#SBATCH -A thermog
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --qos=normal
#SBATCH --gres=gpu:4
#SBATCH -J charmb6825nt12

cd /hpcgpfs01/work/lqcd/thermoG/rlarsen/charm_runs/Nt12_charm_b6825/densl4812f21b6825m00161m0436_548/Run1/Set1/

module load gcc/5.3.0
module load mvapich2

srun gpu_dens do_arg dens_arg 10 trlan_arg
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
