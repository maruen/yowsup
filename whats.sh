#!/bin/bash
NUMBER=$1
MESSAGE=$2
CMMD=`yowsup-cli demos -c /home/bananapi/Local/yowsup/configs/VIVO-01.cfg -s ${NUMBER} "${MESSAGE}"`
echo "${CMMD}"
