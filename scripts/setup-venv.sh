#!/bin/bash

# Author: Dylan Turner
# Description: Creates and installs all needed packages

python3.9 -m pip install virtualenv

python3.9 -m virtualenv .venv
chmod +x .venv/bin/activate
source .venv/bin/activate
pip3 install pip --upgrade
pip3 install -r bgrm/requirements.txt --no-cache-dir
deactivate
