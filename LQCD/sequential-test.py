#!/usr/bin/env python

# This script is for running LQCD test jobs through PanDA
#

import sys
import time
import commands
import json
import subprocess

import userinterface.Client as Client
from taskbuffer.JobSpec import JobSpec
from taskbuffer.FileSpec import FileSpec

class SequentialLQCDSubmitter(object):
	def __init__(self, site):
		self.__site = site
		self.__joblist = {}

	def addJob(self, name, job_desc):
		if name in self.__joblist:
			return false
		self.__joblist[name] = [job_desc, None]
		return true

	def submit(self):
		#route = ["a->b", "b->c", "d->b", "c->e"]
		route = []
		cmd = "dot | grep -v -e \"}\" -e width -e \"\\->\" -e graph -e node | sed -e 's/\[pos=.\+;//' -e 's/\[height=.\+$//' -e 's/,$//' | sed  -E -e '$!N;s/\\n/ /' -e 's/pos=\"[0-9]+,//' -e 's/\",//' | sort -k 2 -n -r | cut -f1 -d' '"

		for j in self.__joblist:
			if self.__joblist[j].cmtConfig is not None and self.__joblist[j].cmtConfig <> '':
				depends_on = j.cmtConfig.split(',')
				for d in depends_on:
					route.append("{} -> {}".format(d, j))

		# TBC

		p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)

		routes = "\n".join(route)
		digraph = "digraph\n{\n%s\n}\n" % routes
		grep_stdout = p.communicate(input=digraph)[0]
		output = grep_stdout.decode().split("\n")
		for o in output:
			depends_on = self.__joblist[o].cmtConfig.split(',')			
			output_dependency = []
			for d in depends_on:
				if self.__jobs[d][1] is not None:
					output_dependency.append(self.__jobs[d][1])
			self.__joblist[o].cmtConfig = ",".join(output_dependency)

			dep_submitted = self.__submit(o)
			if dep_submitted==-1 or dep_submitted=='':
				pass
				# or not!!!!!11111
			self.__jobs[o][1] = dep_submitted


	def __submit(self, name):
		# gets name of job
		# submits
		# returns PanDA id
		if name is None or name not in self.__joblist:
			return -1
		s,o = Client.submitJobs([job],srvID=aSrvID)
		print s
		print o
		for x in o:
			print "PandaID=%s" % x[0]
			return x[0]






aSrvID = None

for idx,argv in enumerate(sys.argv):
    if argv == '-s':
        aSrvID = sys.argv[idx+1]
        sys.argv = sys.argv[:idx]
        break

site = 'ANALY_ORNL_Titan_LQCD'

datasetName = 'panda.destDB.%s' % commands.getoutput('uuidgen')
destName    = 'local'

job_route = {}


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
		"nodes" : 10,
		"walltime" : "02:00:00",
		"name" : "lqcd-test",
		"command" : """
cd /lustre/atlas1/nph109/proj-shared/forPSV

echo "-----------------------------------------------------"
echo "Start job: `date`"
echo "-----------------------------------------------------"
echo "aprun -n 10 -N 1 ./wrapper"
aprun -n 10 -N 1 ./wrapper
echo "-----------------------------------------------------"
echo "End job: `date`"
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

job_route['A'] = job

# =========================


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
		"nodes" : 1,
		"walltime" : "01:10:00",
		"name" : "lqcd-test",
		"command" : """
aprun -n 16 sleep 3600
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

job_route['B'] = job

# =========================

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
		"nodes" : 10,
		"walltime" : "02:00:00",
		"name" : "lqcd-test",
		"command" : """
cd /lustre/atlas1/nph109/proj-shared/forPSV

echo "-----------------------------------------------------"
echo "Start job: `date`"
echo "-----------------------------------------------------"
echo "aprun -n 10 -N 1 ./wrapper"
aprun -n 10 -N 1 ./wrapper
echo "-----------------------------------------------------"
echo "End job: `date`"
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

job.cmtConfig = "A,B"

job_route['C'] = job

# =========================

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
		"nodes" : 1,
		"walltime" : "00:05:00",
		"name" : "lqcd-test",
		"command" : """
aprun -n 1 date
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

job.cmtConfig = "C"

job_route['D'] = job
print(job_route)

sys.exit(0)


# =========================


for i in range(1):
	s,o = Client.submitJobs([job],srvID=aSrvID)
	print s
	print o
	for x in o:
		print "PandaID=%s" % x[0]
