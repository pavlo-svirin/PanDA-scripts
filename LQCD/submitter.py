#!/usr/bin/env python

# This script is for running LQCD test jobs through PanDA
#

import os
import yaml
import sys
import time
import commands
import json
import subprocess
import random

import userinterface.Client as Client
from taskbuffer.JobSpec import JobSpec
from taskbuffer.FileSpec import FileSpec

class SequentialLQCDSubmitter:
	transformation = '#json#'
	datasetName = 'panda.destDB.%s' % commands.getoutput('uuidgen')
	destName    = 'local'
	repr_cmd = "perl /data/psvirin/graph-easy.pl"
	prodSourceLabel = 'user'
	currentPriority = 1000

	def __init__(self, aSrvID, site, vo):
		self.__aSrvID = aSrvID
		self.__joblist = []
		self.site = site
		self.vo = vo

	def createJob(nodes, walltime, command, inputs = None, name = ""):
		job = JobSpec()
		job.jobDefinitionID   = int(time.time()) % 10000
		job.jobName           = "%s" % commands.getoutput('uuidgen')
		job_desc.VO = self.vo
		job_desc.transformation = self.transformation

		job.destinationDBlock = self.datasetName
		job.destinationSE     = self.destName
		job.currentPriority   = self.currentPriority
		job.prodSourceLabel   = self.prodSourceLabel
		job.computingSite     = self.site

		lqcd_command = {
				"nodes" : nodes,
				"walltime" : walltime,
				"name" : name,
				"command" : command
				}

		job.jobParameters = json.dumps(lqcd_command)

		fileOL = FileSpec()
		fileOL.lfn = "%s.job.log.tgz" % job.jobName
		fileOL.destinationDBlock = job.destinationDBlock
		fileOL.destinationSE     = job.destinationSE
		fileOL.dataset           = job.destinationDBlock
		fileOL.type = 'log'
		job.addFile(fileOL)
		job.cmtConfig = inputs

		return job

	def addJob(self, name, job_desc, nextJob=None):
		if name in self.__joblist:
			return False
		if job_desc.cmtConfig==name: # job depends on itself
			return False
		job_desc.cmtConfig = json.dumps({'name' : name, 'next' : nextJob})
		#self.__joblist[name] = [job_desc, None]
		self.__joblist.append(job_desc)
		return True

	def __repr__(self):
		routes = []
		for i in self.__joblist:
			if i.cmtConfig is not None:
				js = json.loads(i.cmtConfig)
				if js['next'] is not None:
					routes.append("[{0}]->[{1}]".format(js['name'], js['next']))
				else:
					routes.append("[{0}]".format(js['name']))

		route_str = " ".join(routes)
		p = subprocess.Popen(self.repr_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
		stdo = p.communicate(input=route_str)[0]
		output = stdo.decode()
		return output

	def submit(self):
		for i in self.__joblist:
			print i.cmtConfig
		self.__submit()


	def __submit(self, name):
		# gets name of job
		# submits
		# returns PanDA id
		if name is None or name not in self.__joblist:
			return -1
		s,o = Client.submitJobs([self.__joblist[name][0]],srvID=self.__aSrvID)
		print s
		print o
		for x in o:
			print "PandaID=%s" % x[0]
			return x[0]
		#return str(random.randint(1,100))


	def __submit(self):
		s,o = Client.submitJobs(self.__joblist,srvID=self.__aSrvID)
		print s
		print o
		for x in o:
			print "PandaID=%s" % x[0]
			return x[0]


class PandaJobsYAMLParser:
    def __init__(self):
        pass

    @staticmethod
    def parse(filename):
        if filename is None or filename == "":
            raise OSError("filename is empty")
        with open(filename, "r") as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
		return None

# read yaml description

jobdef = None

if len(sys.argv) == 1:
    print("No YAML file supplied")
    sys.exit(0)

try:
    jobdef = PandaJobsYAMLParser.parse(sys.argv[1])
    print(jobdef)
except:
    print("Failed")
    sys.exit(1)

aSrvID = None

#for idx,argv in enumerate(sys.argv):
#    if argv == '-s':
#        aSrvID = sys.argv[idx+1]
#        sys.argv = sys.argv[:idx]
#        break

if jobdef is None or len(jobdef)==0:
	print("Nothing to submit")
	sys.exit(0)

sls = SequentialLQCDSubmitter(aSrvID, 'ANALY_ORNL_Titan_LQCD', "lqcd")

for name, descr in jobdef['jobs']:
	inputs = None
	# define outputs
	outputs = None
	if jobdef['sequence'][name] is not None:
		outputs = jobdef['sequence'][name]
	job = sls.createJob(name=name, walltime=descr['walltime'], command=descr['command'], nodes=descr['nodes'], inputs=None)
	sls.addJob(name, job, outputs) 

print(sls)	

sys.exit(0)

# =================================================================
# =================================================================
# =================================================================


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
		"nodes" : 1,
		"walltime" : "00:10:00",
		"name" : "lqcd-test",
		"command" : """
cd /lustre/atlas1/nph109/proj-shared/forPSV

echo "-----------------------------------------------------"
echo "Start job: `date`"
echo "-----------------------------------------------------"
aprun -n 1 date
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

#job_route['A'] = job
sls.addJob('A', job, 'C')

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
		"walltime" : "00:10:00",
		"name" : "lqcd-test",
		"command" : """
aprun -n 16 sleep 300
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

#job_route['B'] = job
sls.addJob('B', job, 'C')

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
		"walltime" : "00:10:00",
		"name" : "lqcd-test",
		"command" : """
cd /lustre/atlas1/nph109/proj-shared/forPSV

echo "-----------------------------------------------------"
echo "Start job: `date`"
echo "-----------------------------------------------------"
aprun -n 10  date
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

#job_route['C'] = job
sls.addJob('C', job, 'D')

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

job.cmtConfig = "C,E"

#job_route['D'] = job
sls.addJob('D', job)


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


#job_route['D'] = job
sls.addJob('E', job, 'D')

print(sls)
print("Now submitting.....")
sls.submit()


sys.exit(0)

