import time
from config_data import GetVar
from util import GetConfig
from runtestinstances import RunInstancesTest
from runsnapshot import RunSnapshot
from logger import Logger
from options import Options
from cleanup import CleanUp


__init__ = 'main'
get_options = Options()
data=get_options.arg_parse()
config = GetVar(getattr(data,"tenant"))
var_ = GetConfig()
log = Logger()
test = RunInstancesTest()
clear = CleanUp()
startTime = time.time()

def runTest1():
    test_name = var_._randomName()
    print "Running Instances and Snapshot Test"
    if test.preTestCheck(config)!=None:
        msg = "Pre Check passed, running instances test"
        log.log_data(config.log_file,msg,"INFO")
        run_result = test.runTest(config,test_name)
        if run_result!=None:
            msg = "Instances test completed, proceed with snapshot"
            log.log_data(config.log_file,msg,"INFO")
            print msg
            snap = RunSnapshot().runSnapshot(config,run_result,test_name)
            if snap!=None:
                msg = "Snapshot Test passed, Test completed sucessfully"
                log.log_data(config.log_file,msg,"INFO")
                print msg
                
                msg = "Test Successful, took %r seconds to complete " % (time.time()-startTime)
                log.log_data(config.log_file,msg,"INFO")
                print msg
                
                msg = "Running Cleaning up"
                log.log_data(config.log_file,msg,"INFO")
                print msg
                
                msg = "Terminating Instances"
                log.log_data(config.log_file,msg,"INFO")
                print msg
                clear.removeInstances(config, run_result)
                
                msg = "Removing Snapshot"
                log.log_data(config.log_file,msg,"INFO")
                print msg
                clear.removeSnapshot(config, snap)
                
                
                msg = "Removing Security Groups and Keypair in next 10 seconds"
                log.log_data(config.log_file,msg,"INFO")
                misc = {'sg':test_name,'kp':test_name}
                time.sleep(int(config.timeout))
                clear.removeMisc(config,misc)
                
                msg = "Clean Up complete, exiting test"
                log.log_data(config.log_file,msg,"INFO")
                print msg               
                         
                raise SystemExit
            
            else:
                msg = "Run instances test failed, exiting test"
                log.log_data(config.log_file,msg,"ERROR")
                print msg
                raise SystemExit
        else:
            msg = "Pre Check failed, test halted"
            log.log_data(config.log_file,msg,"ERROR")
            print msg
            raise SystemExit
  

def runTest2():
    test_name = var_._randomName()
    print "Running Instances Test"
    if test.preTestCheck(config)!=None:
        msg = "Pre Check passed, running instances test"
        log.log_data(config.log_file,"INFO")
        run_result = test.runTest(config,test_name)
        if run_result!=None:
            msg = "Instances test passed, test took %s to complete" % (time.time()-startTime) 
            log.log_data(config.log_file,msg,"INFO")
            print msg
            
            msg = "Running Cleaning up"
            log.log_data(config.log_file,msg,"INFO")
            print msg
            
            msg = "Terminating Instances"
            log.log_data(config.log_file,msg,"INFO")
            print msg
            clear.removeInstances(config, run_result)
            
            msg = "Removing Security Groups and Keypair in next 10 seconds"
            log.log_data(config.log_file,msg,"INFO")
            misc = {'sg':test_name,'kp':test_name}
            time.sleep(int(config.timeout))
            clear.removeMisc(config,misc)
            
            msg = "Clean Up complete, exiting test"
            log.log_data(config.log_file,msg,"INFO")
            print msg  
            
            
            
            raise SystemExit
        else:
            msg = "Run instances test failed, exiting test"
            log.log_debug(config.log_name,msg,"ERROR")
            raise SystemExit
        
    else:
        msg = "Pre Check failed,test halted"
        raise SystemExit
  


def runTest3():
    raise SystemExit

    
select = { 0 : runTest1,
           1 : runTest2,
           2 : runTest3,          
         }




if getattr(data,'all')==True and getattr(data,'instances')==False:
    select[0]()
elif getattr(data,'all')==False and getattr(data,'instances')==True:
    select[1]()
else:
    select[2]()
   
