#!/bin/bash
LINE=$1
CMMD=`./yowsup-cli registration --requestcode sms --phone 55${LINE} --cc 55 --mcc 724 --mnc 30`
