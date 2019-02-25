import os
import sys
import config

## CORREGIR LA SALIDA DEL LOG, SE REPITE EL STATUS SERVICE
def start_service(python, process_name):
    if status_service(process_name):
        pid = os.popen("ps aux | grep " + process_name + " | grep -v 'grep' | awk '{print $2}'").readlines()
        pid = str(pid[0])
        log.info("Start Service: The service could not be started because it already exists - PID {0}".format(pid))
        return False
    else:
        try:
            os.system(python + " " + process_name + " &")
            pid = os.popen("ps aux | grep " + process_name + " | grep -v 'grep' | awk '{print $2}'").readlines()
            pid = str(pid[0])
            log.info("Start Service: The twitter service is started - PID {0}".format(pid))
            return True
        except Exception as err:
            log.error("Start Service: There was an error trying to start the service.")
            log.error(err.args)
            return False


def stop_service(process_name):
    if status_service(process_name):
        pid = os.popen("ps aux | grep " + process_name + " | grep -v 'grep' | awk '{print $2}'").readlines()
        pid = str(pid[0])
        try:
            os.system("kill -TERM " + pid)
        except Exception as err:
            log.error("Stop Service: You can not stop the service, verify that your user has sufficient privileges")
            log.error(err.args)
            return False
        if not status_service(process_name):
            log.info("Stop Service: The service was successfully stopped")
            return True


def restart_service(python_path, process_name):
    log.info("========= Restart Service =========")
    stop_service(process_name)
    start_service(python_path, process_name)
    status_service(process_name)
    log.info("===================================")


def status_service(process_name):
    process = os.popen("ps aux | grep " + process_name + " | grep -v 'grep' | awk '{print $2}' | wc -l").readlines()
    if int(process[0]) > 0:
        pid = os.popen("ps aux | grep " + process_name + " | grep -v 'grep' | awk '{print $2}'").readlines()
        pid = pid[0]
        log.info("Status Service: The twitter service is started - PID {0}".format(pid))
        return True
    else:
        log.info("Status Service: The twitter service isn't started")
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


try:
    # Get parameter
    param = str(sys.argv[1])
    if param.lower() == "start":
        if not start_service(python_path, process_name):
            exit(1)
    elif param.lower() == "stop":
        if not stop_service(process_name):
            exit(1)
    elif param.lower() == "status":
        #if not status_service(process_name):
        #    log.info("Status Service: The twitter service isn't started")
        #else:
        #    log.info("Status Service: The twitter service is started - PID {0}".format(pid))
        pass
    elif param.lower() == "restart":
        if not restart_service(python_path, process_name):
            exit(1)
    else:
        print("Invalid syntax! Remember to use start, stop, restart or status")

except Exception as err:
    log.error(err.args)

#   pid = os.popen("ps aux | grep JPE_Twitter/bin/twitter.py | awk '{print $2}'").readlines()[0] #call pid
#   print(pid)
#   os.system('kill -TERM '+pid)