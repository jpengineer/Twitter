# -*- coding: utf-8 -*-
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#                                                                                                                     //
#   Author: Juan Alejandro Perez Chadia                                                                               //
#   Date: 01-Sep-2018                                                                                                 //
#   Version: V1.0.A                                                                                                     //
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


import os
import sys
import config
import splunk.Intersplunk
#import traceback

#__PACKAGES__ = os.path.dirname(os.path.abspath(__file__)) + "/packages"
#sys.path.append(__PACKAGES__)

_version_ = '1.0.A'
_author_ = 'Juan Alejandro Perez Chandia'
_brand_ = 'JPEngineer'
_type_ = 'Developing'


def start_service(python, process_name):
    if status_service(process_name):
        pid = get_pid(process_name)
        log.info("Start Service: The service could not be started because it already exists - PID {0}".format(pid))
        return False
    else:
        try:
            os.system(python + " " + process_name + " &")
            pid = get_pid(process_name)
            log.info("Start Service: The twitter service is started - PID {0}".format(pid))
            return True
        except Exception as err:
            log.error("Start Service: There was an error trying to start the service.")
            log.error(err.args)
            return False


def stop_service(process_name):
    if status_service(process_name):
        pid = get_pid(process_name)
        try:
            os.system("kill -TERM " + pid)
        except Exception as err:
            log.error("Stop Service: You can not stop the service, verify that your user has sufficient privileges")
            log.error(err.args)
            return False
        if not status_service(process_name):
            log.info("Stop Service: The service was successfully stopped")
            return True
    else:
        log.info("Stop Service: The twitter service isn't started")


def restart_service(python, process_name):
    # log.info("========= Restart Service =========")
    stop_service(process_name)
    start_service(python, process_name)
    status_service(process_name)
    # log.info("===================================")


def status_service(process_name):
    process_count = os.popen("ps aux | grep " + process_name + " | grep -v 'grep' | awk '{print $2}' | wc -l").readlines()
    if int(process_count[0]) > 0:
        return True
    else:
        return False


def get_pid(process_name):
    pid = os.popen("ps aux | grep " + process_name + " | grep -v 'grep' | awk '{print $2}'").readlines()
    return pid[0].replace('\n', '')


# Initial Configurations
path = os.getcwd()
process = path + "/twitter.py"
python_path = "/opt/splunk/bin/python"
log_file = os.path.splitext(os.path.basename(__file__))[0] + '.log'

# Log Configurations
path_log = os.getcwd() + '/logs/'
conf = config.InitialConfig('twitter.conf')
if conf.load_config():
    logger = config.Log(log_file)
    log = logger.config_log(path_log, conf.log_max_bkp, conf.log_max_mb)
else:
    print("Failed Config Load")


try:
    # Get parameter
    # param = str(sys.argv[1])

    sys.argv.insert(1, "__EXECUTE__")
    (isgetinfo, sys.argv) = splunk.Intersplunk.isGetInfo(sys.argv)
    results = splunk.Intersplunk.readResults(None, None, True)
    param = sys.argv[1]

    if param.lower() == "start":
        start_service(python_path, process)
        # if not start_service(python_path, process):
            # exit(1)
    elif param.lower() == "stop":
        stop_service(process)
        # if not stop_service(process):
            # exit(1)
    elif param.lower() == "status":
        if not status_service(process):
            # splunk.Intersplunk.outputResults(results)
            log.info("Status Service: The twitter service isn't started")
        else:
            pid = get_pid(process)
            # splunk.Intersplunk.outputResults("Status Service: The twitter service is started - PID {0}".format(pid))
            log.info("Status Service: The twitter service is started - PID {0}".format(pid))
        pass
    elif param.lower() == "restart":
        restart_service(python_path, process)
        # if not restart_service(python_path, process):
            # exit(1)
    else:
        print("Invalid syntax! Remember to use start, stop, restart or status")

except Exception as err:
    log.error(err.args)
