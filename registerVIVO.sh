#!/bin/bash
LINE=$1
CODE=$2
CMMD=`./yowsup-cli registration --register ${CODE} --phone 55${LINE} --cc 55`
