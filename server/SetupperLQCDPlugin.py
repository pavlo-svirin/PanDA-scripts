import json

from SetupperPluginBase import SetupperPluginBase


class SetupperLQCDPlugin (SetupperPluginBase):
    # constructor
    def __init__(self,taskBuffer,jobs,logger,**params):
        # defaults
        defaultMap = {}
        SetupperPluginBase.__init__(self,taskBuffer,jobs,logger,params,defaultMap)
        self.jobs_map = {}
	#self._taskBuffer = taskBuffer


    # main
    def run(self):
	self.logger.debug('start LQCD Setupper run()')
        acJobs = []
	self.logger.debug('Jobs count: ' + str(len(self.jobs)))

	nextNames = {}
	prevNames = {}
	jobIDs = {}
	toActivate = []
	for j in self.jobs:
		if j.transformation=='#json#':
			# load JSON from cmtConfig
			if j.cmtConfig is not None and j.cmtConfig<>'':
				self.logger.debug('JSON: ' + j.cmtConfig)
				jobData = json.loads(j.cmtConfig)
				if jobData['name'] not in prevNames:
					prevNames[jobData['name']] = []
				if jobData['next'] is not None:
					if not isinstance(jobData['next'], list):
						# has only one successor
						self.logger.debug("Last stage: one successor")
						if jobData['next'] not in prevNames:
							prevNames[jobData['next']] = [jobData['name']]
						else:
							prevNames[jobData['next']].append(jobData['name'])
					else:
						# it is a list
						self.logger.debug("Last stage: multiple successors")
						for n in jobData['next']:
							if n not in prevNames:
								prevNames[n] = [jobData['name']]
							else:
								prevNames[n].append(jobData['name'])
			jobIDs[jobData['name']] = [j, jobData]
		else:
			toActivate.append(j)

	self.logger.debug(str(prevNames))

	self.logger.debug("Now picking jobs to ba activated")
	for n, cnt in prevNames.items():
		if len(cnt)==0:
			toActivate.append(jobIDs[n][0])
	
	self.logger.debug("We got jobs defined to be activated")

	for name, j in jobIDs.items():
		if j[1]['next'] is not None:
			# if single successor
			if not isinstance(j[1]['next'], list):
				j[1]['next'] = jobIDs[j[1]['next']][0].PandaID	# changing names to PandaIDs
			# multiple successors
			else:
				jn = []
				for n in j[1]['next']:
					jn.append(jobIDs[n][0].PandaID)	# changing names to PandaIDs
				j[1]['next'] = jn

		# if fails -> shift block back to right
		j[1]['prev'] = []
		for p in prevNames[name]:
				j[1]['prev'].append(jobIDs[p][0].PandaID)

		self.logger.debug('Serializing JSON')
		self.logger.debug(j[1])

		j[0].cmtConfig = json.dumps(j[1])

		# change 
		self.logger.debug("Now updating job")
		self.taskBuffer.updateJobs([j[0]],inJobsDefined=True,oldJobStatusList=None,extraInfo=None)
		# </block>

	# activate
	self.jobs = toActivate

