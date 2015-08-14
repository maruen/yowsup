#!/bin/bash
LINE=$1
CMMD=`./yowsup-cli demos -c /home/bananapi/Local/yowsup/configs/${LINE}.cfg -r` 
echo ${CMMD}
