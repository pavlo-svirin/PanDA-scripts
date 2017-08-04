#!/usr/bin/env python

#titan_testScript_ec2_alice_2.py
# This script is for running A01_alicegeo through PanDA
#

import sys
import time
import commands
import userinterface.Client as Client
from taskbuffer.JobSpec import JobSpec
from taskbuffer.FileSpec import FileSpec

aSrvID = None

for idx,argv in enumerate(sys.argv):
    if argv == '-s':
        aSrvID = sys.argv[idx+1]
        sys.argv = sys.argv[:idx]
        break

#site = sys.argv[1]
site = 'BNL_KNL_MCORE'
#site = 'BNL-LSST'
#site = 'UKI-NORTHGRID-LANCS-HEP-LSST'
#site = 'UKI-NORTHGRID-MAN-HEP_LSST'
#site = 'ANALY_ORNL_Titan'

datasetName = 'panda.destDB.%s' % commands.getoutput('uuidgen')
destName    = 'local'

job = JobSpec()
job.jobDefinitionID   = int(time.time()) % 10000
job.jobName           = "%s" % commands.getoutput('uuidgen')
# MPI transform on Titan that will run actual job
#Payload for job submission
#job.transformation    = '/bin/date'
job.transformation    = 'python --version'
#job.transformation    = '--version; /bin/date'
#job.transformation    = '--version; '
#job.transformation    = '/cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/phosim.py'
#job.transformation = 'mkdir work output; /bin/date # '
#job.transformation    = 'mkdir work output; python /cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/phosim.py '
#job.transformation    = '--version; mkdir work output; python '
#job.transformation    = '--version; mkdir work output; /lustre/atlas/proj-shared/csc108/app_dir/lsst/software/phosim-phosim_release-0876792bb103/phosim.py '
#job.transformation    = '--version; mkdir work output; echo AAAAA > output/out'
#job.transformation    = '/lustre/atlas/proj-shared/csc108/app_dir/lsst/software/phosim-phosim_release-0876792bb103/phosim.py    /lustre/atlas/proj-shared/csc108/app_dir/lsst/software/phosim-phosim_release-0876792bb103/examples/star  /lustre/atlas/proj-shared/csc108/app_dir/lsst/software/phosim-phosim_release-0876792bb103/phosim/examples/nobackground  -o ./ -w ./'

job.destinationDBlock = datasetName
job.destinationSE     = destName
job.currentPriority   = 1000
job.prodSourceLabel   = 'user'
job.computingSite     = site
#job.jobParameters = ' /lustre/atlas1/nph109/proj-shared/forPSV/ ; ./wrapper'
job.jobParameters = ''
#job.jobParameters     = " /cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/phosim.py    /cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/examples/star -c  /cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/examples/quickbackground"
# job.jobParameters     = " /cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/examples/small_catalog -c  /cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/examples/nobackground "
#job.jobParameters     = " /cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/examples/star "
#job.jobParameters = ""
#job.jobParameters     = " /cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/examples/small_catalog -c  /cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/examples/nobackground "
#job.jobParameters     = " /cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/phosim.py    /cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/examples/small_catalog /cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/examples/quickbackground"
job.VO                = 'lsst'

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
	for x in o:
		print "PandaID=%s" % x[0]
