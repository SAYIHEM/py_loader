#!/bin/bash
dir="/home/pi/py_loader"
cmd="/usr/bin/python3 /home/pi/py_loader/pyloader.py"
user="root"

stdout_log="/home/pi/logs/py_loader.log"
stderr_log="/home/pi/logs/py_loader.err"

sudo -u ${user} ${cmd} >> ${stderr_log} 2>> ${stdout_log} &