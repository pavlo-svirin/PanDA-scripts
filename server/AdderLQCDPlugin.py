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
	self.logger.debug("Running the latest LQCD Adder class")
        from config import panda_config
        passwd = panda_config.dbpasswd
        # initialize cx_Oracle using dummy connection
        from taskbuffer.Initializer import initializer
        initializer.init()
        # instantiate TB
        from taskbuffer.TaskBuffer import taskBuffer
        taskBuffer.init(panda_config.dbhost,panda_config.dbpasswd,nDBConnection=1)

        self.result.setSucceeded()

	if self.job.transformation<>'#json#':
		return

	if self.job.jobStatus=='finished':
		if self.job.cmtConfig is not None and self.job.cmtConfig<>'':
			js = json.loads(self.job.cmtConfig)
			nextJob = js['next']
			activateNext = True
			nextJobDesc = None
			if not nextJob:
				return
			else:
				# we need to check all of the dependencies for next job before activation
				self.logger.debug("nextJob: %s" % nextJob)
				#nextJobDesc = taskBuffer.peekJobs([nextJob],fromDefined=True,fromActive=True,fromArchived=True,fromWaiting=True,forAnal=False)
				nextJobDesc = taskBuffer.peekJobs(nextJob,fromDefined=True,fromActive=True,fromArchived=True,fromWaiting=True,forAnal=False)
				self.logger.debug(str(nextJobDesc))
				#self.logger.debug(nextJobDesc[0].PandaID)

				if nextJobDesc is not None:
					for nj in nextJobDesc:
						activateNext = True
						#depends_on = json.loads(nextJobDesc[0].cmtConfig)
						# <DEBUG>
						if nj.cmtConfig is None:
							#self.logger.debug('cmtConfig for %s is None, retrying...' % nj.PandaID)
							j = taskBuffer.peekJobs([nj.PandaID],fromDefined=True,fromActive=True,fromArchived=True,fromWaiting=True,forAnal=False)
							self.logger.debug('cmtConfig now is %s' % j.cmtConfig)
						# </DEBUG>
						self.logger.debug("Studying next job: %s, its job parameters: %s" % (nj.PandaID, nj.jobParameters))
						self.logger.debug("cmtConfig for the dependent job %s is: %s, its status: %s" % (nj.PandaID, nj.cmtConfig, nj.jobStatus))
						depends_on = json.loads(nj.cmtConfig)
						self.logger.debug("Studying next job: %s, it depends on: %s" % (nj.PandaID, str(depends_on['prev'])))
						# self.logger.debug(str(depends_on['prev']))
						if 'prev' in depends_on and depends_on['prev']:
							self.logger.debug(str(self.job))
							# we are in HOLDING state, but preparing to move to FINISHED
							# no sense to ask about current job
							depends_on['prev'].remove(self.job.PandaID)
							if any(depends_on['prev']):
								self.logger.debug("Checking for the following jobs: %s" % str(depends_on['prev']))
								prevJobs = taskBuffer.peekJobs(depends_on['prev'],fromDefined=True,fromActive=True,fromArchived=True,fromWaiting=True,forAnal=False)
								self.logger.debug("Got the following info about jobs: %s" % str(prevJobs))
								for pj in prevJobs:
									self.logger.debug("%s is %s" % (pj.PandaID, pj.jobStatus))
									# sometimes it is unknown! DEBUG!!!
									if pj.jobStatus<>'finished':
										activateNext = False

							self.logger.debug("Activate next is: %s" % activateNext)
							if activateNext:
								# taskBuffer.activateJobs([nextJobDesc[0]])
								self.logger.debug("Activating jobs: %s" % [nj])
								activated = taskBuffer.activateJobs([nj])
								self.logger.debug("Activated jobs: %s" % activated)

	elif self.job.jobStatus=='failed':
                self.logger.debug('Running failed branch for job: %s' % self.job.PandaID)
		# check maxAttempts
		if self.job.attemptNr<=self.job.maxAttempt:
			self.logger.debug('Resubmitting job: %s' % self.job.PandaID)
			#retValue = taskBuffer.retryJob(self.job.PandaID, '', getNewPandaID=False, failedInActive=True)
			retValue = taskBuffer.retryJob(self.job.PandaID, '', getNewPandaID=False, failedInActive=False)
			self.logger.debug("Return value: %s" % retValue)
