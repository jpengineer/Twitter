# -*- coding: utf-8 -*-
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#                                                                                                                     //
#   Author: Juan Alejandro Perez Chadia                                                                               //
#   Date: 01-Sep-2018                                                                                                 //
#   Version: V1.0                                                                                                     //
#   Documentations:                                                                                                   //
#       - https://developer.twitter.com/en/docs/tweets/timelines/guides/working-with-timelines                        //
#       - https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline.html        //
#       - http://docs.tweepy.org/en/v3.5.0/                                                                           //
#       - https://stackoverflow.com/questions/17157753/get-the-error-code-from-tweepy-exception-instance              //
#                                                                                                                     //
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

import os
import sys
import security
import json
import collections
import logging
import logging.handlers
import time

sys.path.append('/opt/splunk/etc/apps/JPE_Twitter/bin/packages')

class InitialConfig(object):

    def config(self):
        try:
            # Define name of config file
            path = os.path.splitext(__file__)[0] + '.json'
            # Instantiate VerifyConfig class
            config = security.VerifyConfig(path)
            # Load the config file
            file = json.loads(open(path).read(), object_pairs_hook=collections.OrderedDict)
            # Security verify
            self.config_file = config.loadConfig(file)
        except Exception as error:
            exit(1)
        return self.config_file


class Log(object):

    def __init__(self, path, file):
        self.path = path
        self.file = file

    def log_setup(self, backup=3):
        log_handler = logging.handlers.RotatingFileHandler(self.path, mode='a', maxBytes=40 * 1024 * 1024, backupCount=backup, encoding=None, delay=0)
        formatter = logging.Formatter(
            '%(asctime)s ' + self.file + ' %(levelname)s [%(process)d]: %(message)s', '%b %d %H:%M:%S')
        formatter.converter = time.localtime  # if you want UTC time
        log_handler.setFormatter(formatter)
        logger = logging.getLogger()
        logger.addHandler(log_handler)
        logger.setLevel(logging.INFO)
        return logger



#==================================================================================
#                                         TEST
#==================================================================================
'''
if __name__== '__main__':
    # Instantiate initConfig
    initConf = InitialConfig()
    # Define the logs path
    path = os.getcwd() + '/logs/'
    log_file = os.path.splitext(os.path.basename(__file__))[0] + '.log'
    config_log = Log()
    log = config_log.log_setup(path + log_file)
    try:
        print "jajajaja"
        log.info("Cargando Configuración Inicial")
        config_file = initConf.config()
        log.info("Configuración Inicial Cargada exitósamente")
    except Exception as error:
        log.error("Error al Cargar la Configuración Inicial")
        log.error(error)
'''
