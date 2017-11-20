import os
import sys
import commands

# exec
def run(inFile,v_onlyTA,v_firstSubmission):
    #import cPickle as pickle
    #try:
    #    # read Jobs from file
    #    f = open(inFile)
    #    jobs = pickle.load(f)
    #    f.close()
    #except:
    #    type, value, traceBack = sys.exc_info()
    #    print("run() : %s %s" % (type,value))
    #    return
    # password
    from config import panda_config
    passwd = panda_config.dbpasswd
    # initialize cx_Oracle using dummy connection
    from taskbuffer.Initializer import initializer
    initializer.init()
    # instantiate TB
    from taskbuffer.TaskBuffer import taskBuffer
    taskBuffer.init(panda_config.dbhost,panda_config.dbpasswd,nDBConnection=1)
    # run Setupper

    # get jobs
    jobs = taskBuffer.getJobs(1000000,'ANALY_ORNL_Titan_LQCD', 'user',None,None,None,None,
                None,None,None,None,None,None, None)

    #jobs = taskBuffer.getJobs(1000000,'ANALY_ORNL_Titan_LQCD', 'user',cpu,mem,diskSpace,node,timeout,computingElement,
    #            atlasRelease,prodUserID,getProxyKey,countryGroup,workingGroup,allowOtherCountry,
    #            taskID)
    from dataservice.Setupper import Setupper
    thr = Setupper(taskBuffer,jobs,onlyTA=v_onlyTA,firstSubmission=v_firstSubmission)
    thr.start()
    thr.join()
    return


# exit action
def _onExit(fname):
    commands.getoutput('rm -rf %s' % fname)
        

####################################################################
# main
def main():
    import getopt
    import atexit
    # option class
    class _options:
        def __init__(self):
            pass
    options = _options()
    del _options
    # set default values
    options.inFile  = ""
    options.onlyTA  = False
    options.firstSubmission = True
    # get command-line parameters
    try:
        opts, args = getopt.getopt(sys.argv[1:],"i:tf")
    except:
        print("ERROR : Invalid options")
        sys.exit(1)    
    # set options
    for o, a in opts:
        if o in ("-i",):
            options.inFile = a
        if o in ("-t",):
            options.onlyTA = True
        if o == "-f":
            options.firstSubmission = False
    # exit action
    atexit.register(_onExit,options.inFile)
    # run
    run(options.inFile,options.onlyTA,options.firstSubmission)
    # return
    sys.exit(0)


if __name__ == "__main__":
    main()
