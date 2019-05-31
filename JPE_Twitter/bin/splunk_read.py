import traceback
import splunk.Intersplunk
import sys
import os
import config
import ConfigParser
sys.path.append('/opt/splunk/etc/apps/JPE_Twitter/bin/packages/')

_version_ = '1.0.A'
_author_ = 'Juan Alejandro Perez Chandia'
_brand_ = 'JPEngineer'
_type_ = 'Developing'


def write_config(section, option, value, file_name):
    _configParser.read(file_name)
    if _configParser.has_option(section, option):
        _configParser.set(section, option, value)
        with open(file_name, 'wb') as configfile:
            _configParser.write(configfile)
        configfile.close()
    else:
        log.error('[{0}] section or "{1}" option doesn\'t exist'.format(str(section), str(option)))


def verify(param):
    result = False
    if (param[0].lower() == 'true' and len(param[5]) > 1) or param[0].lower() == 'false':
        if len(param[1]) > 1 and len(param[2]) > 1 and len(param[3]) > 1 and len(param[4]) > 1 :
            result = True
    return result

path = os.getcwd() + '/logs/'
log_file = os.path.splitext(os.path.basename(__file__))[0] + '.log'
logger = config.Log(log_file)
conf = config.InitialConfig('twitter.conf')
log = logger.config_log(path, conf.log_max_bkp, conf.log_max_mb)

sys.argv.insert(1, "__EXECUTE__")
(isgetinfo, sys.argv) = splunk.Intersplunk.isGetInfo(sys.argv)
results = splunk.Intersplunk.readResults(None, None, True)


# R E A D   S P L U N K   A R G U M E N T S
'''
#     arg[0] = Encrypt --> (true or false)
#     arg[1] = consumer_key
#     arg[2] = consumer_secret
#     arg[3] = access_token
#     arg[4] = access_secret
#     arg[5] = key --> Only if arg[0] is true
'''

if len(sys.argv) > 1:
    arg = []
    for x in sys.argv[1:]:
        arg.append(x)

    if not verify(arg):
        log.error("Please, complete all fields.")
        exit(0)

    try:
        _configParser = ConfigParser.SafeConfigParser()
        write_config('token', 'consumer_key', arg[1], 'twitter.conf')
        write_config('token', 'consumer_secret', arg[2], 'twitter.conf')
        write_config('token', 'access_token', arg[3], 'twitter.conf')
        write_config('token', 'access_secret', arg[4], 'twitter.conf')

        if arg[0].lower() == 'true':
            write_config('security', 'encryption', arg[0], 'twitter.conf')
            write_config('security', 'key', arg[5], 'twitter.conf')
        else:
            # TODO Revisar
            write_config('security', 'encryption', arg[0], 'twitter.conf')
            write_config('security', 'key', 'None', 'twitter.conf')
            log.warn("The configuration isn't encrypted")

        log.info("Token saved successfully")

    except Exception as error:
        log.error("The token could not be saved")
        log.error(traceback.format_exc())

else:
    log.error("Please, validate the setting on titter.conf")
    sys.exit(1)

# ==================================================================================
#                           T  E  S  T  I  N  G
# ==================================================================================

# if __name__ == "__main__":
#     print('Ejecutando como programa principal')
#     write_config('token', 'consumer_key', 'jujujujuj', 'twitter.conf')
