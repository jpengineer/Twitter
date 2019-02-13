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
sys.path.append('/opt/splunk/etc/apps/JPE_Twitter/bin/packages')

import json
import base64
import hashlib
from Crypto.Cipher import AES

class AESCipher(object):

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        #iv = Random.new().read(AES.block_size)
        iv = "Tn/wvw0X7CmW7Q=="
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


class VerifyConfig(object):

    def __init__(self, path):
        self.path = path

    def loadConfig(self, config):
        self.config = config
        # verify the key
        key = self.config['KEY'].encode('utf-8')
        new_key = verify_key(key, self.config, self.path)

        if self.config['ENCRYPT'].lower() == "true":
            #Instantiate EncryptionAES Class
            EA = AESCipher(new_key)
            #Encrypt the parameters of configuration
            for x in self.config:
                if x != "KEY" and x != "USERS_TARGET" and x != "ENCRYPT" and x != "NUM_TWEETS" and x != "TYPE" and x != "FILTER":
                    self.config[x] = EA.encrypt(self.config[x])
            # Change the value of encrypt parameter
            self.config['ENCRYPT'] = "false"
            # Save the new config
            self.config = (open(self.path, 'w+')).write(json.dumps(self.config))
        return self.config


def verify_key(key, config, path):
    # Define internal key
    magic_word = "i_dont_remember_the_magic_word"
    # Encryption key
    internal_key = "I_call_the_big_one_CUCA"
    # Instantiate the EncryptionAES class with internal_key
    internal_EA = AESCipher(internal_key)
    # Check if magic_word is inside the key
    try:
        if magic_word in internal_EA.decrypt(key):
            return key
        else:
            # If magic_word isn't inside the key then add and generate the new key
            key = internal_EA.encrypt(magic_word + key)
            # Save the new key
            config['KEY'] = key
            # Update the config file
            config = (open(path, 'w+')).write(json.dumps(config))
            return key
    except:
        key = internal_EA.encrypt(magic_word + key)
        # Save the new key
        config['KEY'] = key
        # Update the config file
        #config = (open(path, 'w+')).write(json.dumps(config))
        return key
