#!/bin/bash

#load venv
source env/bin/activate

#start before robots
python3 robot/main.py -p 4000 -r before > /dev/null 2>&1 &
python3 robot/main.py -p 4001 -r before > /dev/null 2>&1 & 

#start after robots
python3 robot/main.py -p 4100 -r after > /dev/null 2>&1 &
python3 robot/main.py -p 4101 -r after > /dev/null 2>&1 & 

#start ovens
python3 oven/main.py -p 5000 > /dev/null 2>&1 &
python3 oven/main.py -p 5001 > /dev/null 2>&1 &

echo "robots and ovens started"
deactivate
