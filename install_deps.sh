#!/bin/bash

# create virtual env
python3 -m venv env

# activate virtual env
source env/bin/activate

#install deps
pip3 install -r requirements.txt

# remove virtual env
deactivate

