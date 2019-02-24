import os
import sys
import config

# SERVICE START AND STATUS IT'S OKAY
def start_service(python, process_name):
    if status_service(process_name):
        pid = os.popen("ps aux | grep " + process_name + " | grep -v 'grep' | awk '{print $2}'").readlines()
        pid = str(pid[0])
        log.info("The service could not be started because it already exists - PID {0}".format(pid))
        return False
    else:
        try:
            os.system(python + " " + process_name + " &")
            pid = os.popen("ps aux | grep " + process_name + " | grep -v 'grep' | awk '{print $2}'").readlines()
            pid = str(pid[0])
            log.info("The twitter service is started - PID {0}".format(pid))
            return True
        except Exception as err:
            log.error("There was an error trying to start the service.")
            log.error(err.args)
            return False


def stop_service(param):
    pass


def restart_service(param):
    pass


def status_service(process_name):
    process = os.popen("ps aux | grep " + process_name + " | grep -v 'grep' | awk '{print $2}' | wc -l").readlines()
    if int(process[0]) > 0:
        pid = os.popen("ps aux | grep " + process_name + " | grep -v 'grep' | awk '{print $2}'").readlines()
        pid = pid[0]
        log.info("Service Status: The twitter service is started - PID {0}".format(pid))
        return True
    else:
        log.info("Service Status: The twitter service isn't started")
        return False


# Initial Configurations
path = os.getcwd()
process_name = path + "/twitter.py"
python_path = "/opt/splunk/bin/python"
log_file = os.path.splitext(os.path.basename(__file__))[0] + '.log'


# Log Configurations
conf_file = config.InitialConfig()
config_log = config.Log(path + "/logs/" + log_file, __file__)
log = config_log.log_setup(5)





# Get the total number of args passed to the demo.py
param = str(sys.argv[1])
print(status_service(process_name))


#   pid = os.popen("ps aux | grep JPE_Twitter/bin/twitter.py | awk '{print $2}'").readlines()[0] #call pid
#   print(pid)
#   os.system('kill -TERM '+pid)