# LQCD plugin of Adder for VOs which don't need DDM access
import json

from AdderPluginBase import AdderPluginBase
from pandalogger.PandaLogger import PandaLogger


class AdderLQCDPlugin(AdderPluginBase):
    
    # constructor
    def __init__(self, job, **params):
        AdderPluginBase.__init__(self, job, params)


    # main
    def execute(self):
	self.logger.debug("Running LQCD Adder class")
        from config import panda_config
        passwd = panda_config.dbpasswd
        # initialize cx_Oracle using dummy connection
        from taskbuffer.Initializer import initializer
        initializer.init()
        # instantiate TB
        from taskbuffer.TaskBuffer import taskBuffer
        taskBuffer.init(panda_config.dbhost,panda_config.dbpasswd,nDBConnection=1)

        self.result.setSucceeded()
	if self.job.jobStatus=='finished' and self.job.cmtConfig is not None and self.job.cmtConfig<>'':
		js = json.loads(self.job.cmtConfig)
		nextJob = js['next']
		activateNext = True
		nextJobDesc = None
		if not nextJob:
			return
		else:
			# we need to check all of the dependencies for next job before activation
			nextJobDesc = taskBuffer.peekJobs([nextJob],fromDefined=True,fromActive=True,fromArchived=True,fromWaiting=True,forAnal=False)
			self.logger.debug(str(nextJobDesc))
			self.logger.debug(nextJobDesc[0].PandaID)
			if nextJobDesc is not None:
				depends_on = json.loads(nextJobDesc[0].cmtConfig)
				self.logger.debug("Studying next job, it depends on: ")
				self.logger.debug(str(depends_on['prev']))
				if 'prev' in depends_on and depends_on['prev']:
					self.logger.debug(str(self.job))
					depends_on['prev'].remove(self.job.PandaID)
					prevJobs = taskBuffer.peekJobs(depends_on['prev'],fromDefined=True,fromActive=True,fromArchived=True,fromWaiting=True,forAnal=False)
					for pj in prevJobs:
						self.logger.debug("%s is %s" % (pj.PandaID, pj.jobStatus))
						if pj.jobStatus<>'finished':
							activateNext = False
							#break
		self.logger.debug("Activate next is: %s" % activateNext)
        	if activateNext:
			taskBuffer.activateJobs([nextJobDesc[0]])
