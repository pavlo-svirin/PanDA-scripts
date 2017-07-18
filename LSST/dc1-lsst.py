#!/usr/bin/env python

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

dry_run = False

#site = sys.argv[1]
#site = 'BNL-LSST'
site = 'UKI-NORTHGRID-LANCS-HEP-LSST'
#site = 'UKI-NORTHGRID-MAN-HEP_LSST'
#site = 'ANALY_ORNL_Titan'

#sites = ('BNL-LSST', 'UKI-NORTHGRID-LANCS-HEP-LSST', 'UKI-NORTHGRID-MAN-HEP_LSST')
sites = ['BNL-LSST', 'UKI-NORTHGRID-LANCS-HEP-LSST', 'UKI-NORTHGRID-MAN-HEP_LSST', 'RAL-LCG2_LSST']
#debug
#sites = ['RAL-LCG2_LSST','UKI-NORTHGRID-MAN-HEP_LSST', 'UKI-NORTHGRID-LANCS-HEP-LSST']
#sites = ['BNL-LSST']
#sites = ['UKI-NORTHGRID-LANCS-HEP-LSST']
#sites = ['RAL-LCG2_LSST']

sensors = ['00', '01', '02', '10', '11', '12', '20', '21', '22']
#sensors = ['01']

rafts = ['01', '02', '03', '10', '11', '12', '13', '14', '20', '21', '22', '23', '24', '30', '31', '32', '33', '34', '41', '42', '43']
# debug
#rafts = ['01', '02', '03', '10']
#rafts = ['22']
#rafts = ['03']

directories_template = "/gpfs01/astro/workarea/anze/DC1/cats/%s"

directories = [1487655, 1066760, 704362, 2170875, 1288057, 1014427, 193196, 202612, 40368, 810202]

datasetName = 'panda.destDB.%s' % commands.getoutput('uuidgen')
destName    = 'local'

"""
job = JobSpec()
job.jobDefinitionID   = int(time.time()) % 10000
job.jobName           = "%s" % commands.getoutput('uuidgen')
job.transformation    = 'mkdir work output; python /cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/phosim.py '

job.destinationDBlock = datasetName
job.destinationSE     = destName
job.currentPriority   = 1000
job.prodSourceLabel   = 'user'
job.computingSite     = site
job.jobParameters     = " /cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/examples/small_catalog -c  /cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/examples/nobackground "
job.VO                = 'lsst'

fileOL = FileSpec()
fileOL.lfn = "%s.job.log.tgz" % job.jobName
fileOL.destinationDBlock = job.destinationDBlock
fileOL.destinationSE     = job.destinationSE
fileOL.dataset           = job.destinationDBlock
fileOL.type = 'log'
#job.addFile(fileOL)

#=============
fileD = FileSpec()
fileD.dataset    = 'ddo.000001.Atlas.Ideal.DBRelease.v170602'
fileD.prodDBlock = fileD.dataset
fileD.lfn = 'DBRelease-17.6.2.tar.gz'
fileD.type = 'input'
#job.addFile(fileD)

fileOA = FileSpec()
fileOA.lfn = "%s.HITS.pool.root" % job.jobName
fileOA.destinationDBlock = job.destinationDBlock
fileOA.destinationSE     = job.destinationSE
fileOA.dataset           = job.destinationDBlock
fileOA.destinationDBlockToken = 'ATLASDATADISK'
fileOA.type = 'output'
#job.addFile(fileOA)

#job.addFile(fileOL)
#============
"""

phosim_executable = 'python /cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/phosim.py '
astro_storage_url = 'gsiftp://xrdlsst.sdcc.bnl.gov:2811'
i = 0

#for i in range(len(directories)*len(sensors)*len(rafts)):

jobs = []

for d in directories:
	for r in rafts:
		for sen in sensors:
			job = JobSpec()
			job.jobDefinitionID   = int(time.time()) % 10000
			job.jobName           = "%s" % commands.getoutput('uuidgen')
			job.transformation    = 'mkdir work output %s; ' % d

			job.destinationDBlock = datasetName
			job.destinationSE     = destName
			job.currentPriority   = 1000
			job.prodSourceLabel   = 'user'
			#job.computingSite     = site
			job.computingSite     = sites[i % len(sites)]
			job.VO                = 'lsst'
			fileOL = FileSpec()
			fileOL.lfn = "dc1-%s-%s-%s.job.log.tgz" % (d,r,sen)
			fileOL.destinationDBlock = job.destinationDBlock
			fileOL.destinationSE     = job.destinationSE
			fileOL.dataset           = job.destinationDBlock
			#fileOL.destinationDBlockToken = 'ATLASDATADISK'    
			fileOL.type = 'log'
			job.addFile(fileOL)

                        se_directory = directories_template % d
			#job.jobParameters = 'gfal-copy -r %s%s ./%d/ ; ' % (astro_storage_url, se_directory, d)
			job.jobParameters = """for i in {1..20}; do gfal-copy -t 300 --transfer-timeout 300 -r %s%s file://$(pwd)/%d/ ; if [[ "$?" == "0" ]]; then break; fi; if [[ "$i" -eq "20" ]]; then echo Unable to do stage-in; exit 1; fi; done ; """ % (astro_storage_url, se_directory, d)
			job.jobParameters = job.jobParameters + phosim_executable
			job.jobParameters = job.jobParameters + "%s/phosim_cat_%s.txt -s R%s_S%s -t 8 -o $(pwd)/output -w $(pwd)/work; rm -rf ./%s; #" % (d,d,r,sen,d)
			#job.jobParameters = job.jobParameters + "%s/phosim_cat_%s.txt -s R%s_S%s -o $(pwd)/output -w $(pwd)/work; rm -rf ./%s; #" % (d,d,r,sen,d)

			print job.jobParameters + " site: " + job.computingSite + "\n\n"
			jobs.append(job)
			i = i+1

print "Jobs to be submitted: %d" % i

if dry_run:
	print "Dry run requested....exiting."
	sys.exit(0)

print "Submitting...\n"
s,o = Client.submitJobs(jobs, srvID=aSrvID)
print s

for x in o:
	print "PandaID=%s" % x[0]

print "Jobs submitted: %d" % i





# ===================

# MPI transform on Titan that will run actual job
#Payload for job submission
#job.transformation    = '--version ; /bin/date'
#job.transformation    = '--version; /bin/date'
#job.transformation    = '--version; '
#job.transformation    = '/cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/phosim.py'
#job.transformation = 'mkdir work output; /bin/date # '
#job.transformation    = '--version; mkdir work output; python '
#job.transformation    = '--version; mkdir work output; /lustre/atlas/proj-shared/csc108/app_dir/lsst/software/phosim-phosim_release-0876792bb103/phosim.py '
#job.transformation    = '--version; mkdir work output; echo AAAAA > output/out'
#job.transformation    = '/lustre/atlas/proj-shared/csc108/app_dir/lsst/software/phosim-phosim_release-0876792bb103/phosim.py    /lustre/atlas/proj-shared/csc108/app_dir/lsst/software/phosim-phosim_release-0876792bb103/examples/star  /lustre/atlas/proj-shared/csc108/app_dir/lsst/software/phosim-phosim_release-0876792bb103/phosim/examples/nobackground  -o ./ -w ./'
#job.jobParameters     = " /cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/phosim.py    /cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/examples/star -c  /cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/examples/quickbackground"
#job.jobParameters     = " /cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/examples/star "
#job.jobParameters = ""
#job.jobParameters     = " /cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/examples/small_catalog -c  /cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/examples/nobackground "
#job.jobParameters     = " /cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/phosim.py    /cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/examples/small_catalog /cvmfs/lsst.opensciencegrid.org/panda/phosim-phosim_release-0876792bb103/examples/quickbackground"
