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
	for j in self.jobs:
		# load JSON from cmtConfig
		if j.cmtConfig is not None and j.cmtConfig<>'':
			self.logger.debug('JSON: ' + j.cmtConfig)
			nextData = json.loads(j.cmtConfig)
			if nextData['name'] not in prevNames:
				prevNames[nextData['name']] = []
			if nextData['next'] is not None:
				self.logger.debug("Last stage")
				if nextData['next'] not in prevNames:
					prevNames[nextData['next']] = [nextData['name']]
				else:
					prevNames[nextData['next']].append(nextData['name'])
		jobIDs[nextData['name']] = [j, nextData]

	self.logger.debug(str(prevNames))

	self.logger.debug("Now picking jobs to ba activated")
	toActivate = []
	for n, cnt in prevNames.items():
		if len(cnt)==0:
			toActivate.append(jobIDs[n][0])
	
	self.logger.debug("We got jobs defined to be activated")

	for name, j in jobIDs.items():
		if j[1]['next'] is not None:
			j[1]['next'] = jobIDs[j[1]['next']][0].PandaID	# changing names to PandaIDs
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
"""
        for job in self.jobs:
		if job.computingSite<>'ANALY_ORNL_Titan_LQCD' :
                        acJobs.append(job)
			continue
                self.jobs_map[job.PandaID] = job
        for panda_id in self.jobs_map:
                setToActivated = True
                if job == None or job.jobStatus <> 'defined': #['unknown', 'running', 'starting', 'finished','failed']:
                        continue
                if job.cmtConfig is not None:
                        # split cmtConfig by ,
                        depends_on = job.cmtConfig.split(',')
                        #for dj in depends_on:
                                #if dj in self.jobs_map and jobs_map[dj].jobStatus <> 'finished':
			if depends_on:
				depjob = self.taskBuffer.peekJobs(self, depends_on, fromDefined=True,fromActive=True,fromArchived=True,fromWaiting=False,forAnal=False)
				for d in depjob:
					if d.jobStatus<>'finished':
                                        	setToActivated = False
                if not setToActivated:
                        #acJobs.append(job)
			self.jobs = []

        # activate
	self.logger.debug("We are activating " + str(len(acJobs)) + "jobs")
        self.taskBuffer.activateJobs(acJobs)
"""

    # post run
    #def postRun(self):
    #    pass
