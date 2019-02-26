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
import config
import security
from tweepy import OAuthHandler
from tweepy import API
from tweepy import parsers
from tweepy import StreamListener
from tweepy import Stream
import splunklib.client as client
import socket


sys.path.append('/opt/splunk/etc/apps/JPE_Twitter/bin/packages/')


class Listener(StreamListener):
    def on_data(self, data):
        try:
            data = data.replace('\n', '')
            #log.info(data)
            #return data
            log.info(data.replace('\n', ''))
        except Exception as error:
            log.error(error)


def authentication(cipher, configuration):
    try:
        # Authentication with Twiteer API
        authenticate = OAuthHandler(cipher.decrypt(configuration['CONSUMER_KEY']), cipher.decrypt(configuration['CONSUMER_SECRET']))
        authenticate.set_access_token(cipher.decrypt(configuration['ACCESS_TOKEN']), cipher.decrypt(configuration['ACCESS_SECRET']))
        twitter_api = API(authenticate, parser=parsers.JSONParser())
        return twitter_api, authenticate
    except Exception as err:
        log.error("There was an error trying to connect with twitter.")
        log.error(err.args)
        exit(0)


# Define the log path
path = os.getcwd() + '/logs/'
log_file = os.path.splitext(os.path.basename(__file__))[0] + '.log'

# Load Initial Configurations
conf_file = config.InitialConfig()
config_log = config.Log(path + log_file, __file__)
log = config_log.log_setup(5)
file = conf_file.config()
try:
    key = security.AESCipher(file['KEY'].decode('utf-8'))
except:
    key = security.AESCipher(file['KEY'])

api, auth = authentication(key, file)
log.info("Successful Twitter authentication")

# if file['TYPE'].upper() == "TWEETS":
#     # Extract users from file
#     users = file['USERS_TARGET'].split(',')
#     log.info("USER_TARGET: " + str(users))
#
#     # Extract tweets by users
#     for usr in users:
#         log.info("USER: " + str(usr))
#         print "USERS: ", usr
#         # Verify users config
#         if not usr:
#             log.warning("No existen usuarios configurados. Verificar USERS_TARGET en config.json")
#             print "Check USER_TARGET in config file."
#             break
#         else:
#             tweets = api.user_timeline(screen_name=usr, count=int(file['NUM_TWEETS']), include_rts=False)
#             json.dumps(tweets)
#             log.info(tweets.replace('\n', ''))
#             for message in tweets:
#                 print message['created_at'], " : ", message['text']

if file['TYPE'].upper() == "LISTENER":
    # try:
    #     service = client.connect(host='localhost', port=8089, username='admin', password='Nomeacuerdo', verify=False, submit='http')
    #     splunk_index = service.indexes["twitter"]
    #     splunk_socket = splunk_index.attach(sourcetype='twitter', host=socket.gethostname())
    # except Exception as err:
    #     log.error("Splunk error - Connection refused")
    #     log.error(err.args)
    #     exit(1)

    listener = StreamListener()
    listener = Stream(auth, Listener(), tweet_mode='extended')
    listener.filter(track=[file['FILTER']], languages=["es"])
    #   splunk_socket.send(listener.filter(track=[file['FILTER']], languages=["es"]))
    #   splunk_socket.close()

else:
    log.error("Verify TYPE parameter in the configuration file")
    exit(0)
#except Exception as e:
#    log.error(e)
