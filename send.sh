#!/bin/bash
LINE=$1
NUMBER=$2
MESSAGE=$3
CMMD=`yowsup-cli demos -c /home/bananapi/Local/yowsup/configs/${LINE}.cfg -s ${NUMBER} "${MESSAGE}"`
