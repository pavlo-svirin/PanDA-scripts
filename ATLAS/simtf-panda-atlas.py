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
job.transformation    = 'cp '
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

#job.jobParameters = ' -r /hpcgpfs01/scratch/atlas-test-jobs/inputdata/mc15_13TeV/ .; ln -fs mc15_13TeV/EVNT.05107112._000030.pool.root.1 ./EVNT.05107112._000030.pool.root.1; export ATLAS_SW_BASE=/hpcgpfs01/scratch/atlas-test-jobs/cvmfs/; export ALRB_localConfigDir=$HOME/myLocalConfig; export ALRB_RELOCATECVMFS="YES"; export ATLAS_LOCAL_ROOT_BASE=$ATLAS_SW_BASE/atlas.cern.ch/repo/ATLASLocalRootBase; source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh --quiet; export LD_LIBRARY_PATH=/hpcgpfs01/scratch/atlas-test-jobs/cvmfs/atlas.cern.ch/repo/sw/ldpatch/:$LD_LIBRARY_PATH ; asetup --cmtconfig=x86_64-slc6-gcc49-opt AtlasOffline,21.0.15 ; export ATHENA_PROC_NUMBER=64 ; unset FRONTIER_SERVER; Sim_tf.py --inputEVNTFile="EVNT.05107112._000030.pool.root.1" --maxEvents="64" --postInclude "default:RecJobTransforms/UseFrontier.py" --preExec "EVNTtoHITS:simFlags.SimBarcodeOffset.set_Value_and_Lock(200000)" "EVNTtoHITS:simFlags.TRTRangeCut=30.0; simFlags.TightMuonStepping=True" --preInclude "EVNTtoHITS:SimulationJobOptions/preInclude.BeamPipeKill.py,SimulationJobOptions/preInclude.FrozenShowersFCalOnly.py" --skipEvents="0" --firstEvent="145001" --outputHITSFile="HITS.10932086._001491.pool.root.1" --physicsList="FTFP_BERT_ATL_VALIDATION" --randomSeed="1491" --DBRelease="all:current" --conditionsTag "default:OFLCOND-MC16-SDR-14" --geometryVersion="default:ATLAS-R2-2016-01-00-01_VALIDATION" --runNumber="301040" --AMITag="s3126" --DataRunNumber="284500" --simulator="FullG4" --truthStrategy="MC15aPlus" ; export ; '

job.jobParameters = ' -r /hpcgpfs01/scratch/atlas-test-jobs/inputdata/mc15_13TeV/ .; ln -fs mc15_13TeV/EVNT.05107112._000030.pool.root.1 ./EVNT.05107112._000030.pool.root.1; Sim_tf.py --inputEVNTFile="EVNT.05107112._000030.pool.root.1" --maxEvents="64" --postInclude "default:RecJobTransforms/UseFrontier.py" --preExec "EVNTtoHITS:simFlags.SimBarcodeOffset.set_Value_and_Lock(200000)" "EVNTtoHITS:simFlags.TRTRangeCut=30.0; simFlags.TightMuonStepping=True" --preInclude "EVNTtoHITS:SimulationJobOptions/preInclude.BeamPipeKill.py,SimulationJobOptions/preInclude.FrozenShowersFCalOnly.py" --skipEvents="3936" --firstEvent="145001" --outputHITSFile="HITS.10932086._001491.pool.root.1" --physicsList="FTFP_BERT_ATL_VALIDATION" --randomSeed="1491" --DBRelease="all:current" --conditionsTag "default:OFLCOND-MC16-SDR-14" --geometryVersion="default:ATLAS-R2-2016-01-00-01_VALIDATION" --runNumber="301040" --AMITag="s3126" --DataRunNumber="284500" --simulator="FullG4" --truthStrategy="MC15aPlus" ; export ; '

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
	#s,o = Client.killJobs([i for i in range(8250,8259)], srvID=aSrvID)
	#print s
	#print o
