#!/bin/bash

# Author: Dylan Turner
# Description: Creates and installs all needed packages

pip3 install virtualenv

virtualenv .venv
chmod +x .venv/bin/activate
source .venv/bin/activate
pip3 install -r bgrm/requirements.txt --no-cache-dir
deactivate
