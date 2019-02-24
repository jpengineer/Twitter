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
#       - https://stackoverflow.com/questions/17157753/get-the-error-code-from-tweepy-exception-instance              //                                                           //
#                                                                                                                     //
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

import os
import sys
import config
import security
from tweepy import OAuthHandler
from tweepy import API
from tweepy import parsers
import json
from tweepy import StreamListener
from tweepy import TweepError
from tweepy import Stream

sys.path.append('/opt/splunk/etc/apps/JPE_Twitter/bin/packages/')


class Listener(StreamListener):

    '''Listener Initial Config'''

    # def on_data(self, data):
    #     data = json.loads(data)
    #     print data
    #     try:
    #         print "Contain full_text: ", data['extended_tweet']['full_text'].encode("utf-8")
    #     except:
    #         print "Contain: ", data['text'].encode("utf-8")
    #     print "User Name: ", data['user']['name'].encode("utf-8")
    #     a = api.get_user(data['user']['id'])
    #     print "Twitter User: @" + a['screen_name']
    #     print "Location: ", a['location']
    #     print "============================="
    #     return True

    # def on_status(self, data):
    #     try:
    #         text = str(data.extended_tweet['full_text'].encode('utf-8'))
    #     except:
    #         text = str(data.text.encode('utf-8'))
    #
    #     user_name = str(data._json['user']['name'].encode('utf-8'))
    #     user_account = str(data._json['user']['screen_name'].encode('utf-8'))
    #     log.info("user_name: " + user_name + " user_account: " + user_account + " tweets: " + text)
    #     return True

    def on_data(self, data):
        try:
            log.info(data)
        except Exception as error:
            log.error(error)

    # def on_error(self, data):
    #     log.error(data)

# Define the log path
path = '/opt/splunk/etc/apps/JPE_Twitter/bin/logs/'
log_file = os.path.splitext(os.path.basename(__file__))[0] + '.log'

# Load Initial Configurations
conf_file = config.InitialConfig()
config_log = config.Log(path + log_file, __file__)
file = conf_file.config()
log = config_log.log_setup(5)
try:
    # Load AESCipher
    try:
        cipher = security.AESCipher(file['KEY'].decode('utf-8'))
    except:
        cipher = security.AESCipher(file['KEY'])

    try:
        # Authentication with Twiteer API
        log.info("Conexión con Twitter API")
        auth = OAuthHandler(cipher.decrypt(file['CONSUMER_KEY']), cipher.decrypt(file['CONSUMER_SECRET']))
        auth.set_access_token(cipher.decrypt(file['ACCESS_TOKEN']), cipher.decrypt(file['ACCESS_SECRET']))
        api = API(auth, parser=parsers.JSONParser())

        # Verify Authentication
        verify = api.verify_credentials()
        log.info("Autenticación Twitter Exitosa")
    except:
        log.error("Error al conectar con Twitter, verificar las credenciales.")


    if file['TYPE'].upper() == "TWEETS":
        # Extract users from file
        users = file['USERS_TARGET'].split(',')
        log.info("USER_TARGET: " + str(users))

        # Extract tweets by users
        for usr in users:
            log.info("USER: " + str(usr))
            print "USERS: ", usr
            # Verify users config
            if not usr:
                log.warning("No existen usuarios configurados. Verificar USERS_TARGET en config.json")
                print "Check USER_TARGET in config file."
                break
            else:
                tweets = api.user_timeline(screen_name=usr, count=int(file['NUM_TWEETS']), include_rts=False)
                json.dumps(tweets)
                log.info(tweets)
                for message in tweets:
                    print message['created_at'], " : ", message['text']

    elif file['TYPE'].upper() == "LISTENER":
        listener = StreamListener()
        listener = Stream(auth, Listener(), tweet_mode='extended')
        #print file['FILTER']
        listener.filter(track=[file['FILTER']])

    else:
        log.error("Verificar parametro TYPE en el archivo de configuración. Debe ir Listener o Tweets")

#except TweepError as e:
#    log.error(e.message[0]['code'])
#    log.error(e.args[0][0]['code'])

except Exception as e:
    log.error(e)
