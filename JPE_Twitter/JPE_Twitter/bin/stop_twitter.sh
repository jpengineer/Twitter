#!/bin/bash

if (( $(ps -ef | grep -v grep | grep 'JPE_Twitter/bin/twitter.py' | wc -l) > 0 ))
then
  pid=$(ps aux | grep 'JPE_Twitter/bin/twitter.py'  | grep -v 'grep' | awk '{print $2}')
  kill -9 $pid
  echo "Servicio Detenido Correctamente" >> /opt/splunk/etc/apps/JPE_Twitter/bin/logs/twitter.log 2>&1 &
else
  echo "El Servicio se Encuentra Detenido" >> /opt/splunk/etc/apps/JPE_Twitter/bin/logs/twitter.log 2>&1 &
fi
