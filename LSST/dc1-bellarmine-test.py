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

site = 'Bellarmine-LSST'

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
job.cmtConfig = json.dumps({'name' : 'BBBB', 'next' : None})

lqcd_command = {
		"nodes" : 1,
		"walltime" : "03:00:00",
		"name" : "lqcd-test",
		"next" : None,
		"command" : """
. $OSG_GRID/setup.sh

hostname -f
which gfal-copy
echo ============
#ls -lR /cvmfs/lsst.opensciencegrid.org
echo ===========
#time gfal-copy -t 300 --transfer-timeout 300 -r gsiftp://xrdlsst.sdcc.bnl.gov:2811/gpfs01/astro/workarea/anze/DC1/cats/810202 $(pwd)

mkdir work output

for i in {1..20}; do
 gfal-copy -v -t 300 --transfer-timeout 300 -r gsiftp://xrdlsst.sdcc.bnl.gov:2811/gpfs01/astro/workarea/anze/DC1/cats/2170875 file://$(pwd)/2170875/ ;
 if [[ "$?" == "0" ]]; then break;
 fi;
  if [[ "$i" -eq "20" ]]; then echo Unable to do stage-in; exit 1; fi; done ;
python /cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/phosim.py 2170875/phosim_cat_2170875.txt -s R21_S10 -t 8 -o $(pwd)/output -w $(pwd)/work; rm -rf ./2170875;
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
