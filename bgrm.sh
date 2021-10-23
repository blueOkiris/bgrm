#!/bin/bash

# Author: Dylan Turner
# Description: Run everything

if [ $(id -u) != "0" ]; then
    echo "You need to be root to run this script!"
    exit 1
fi

if [ ! -f "v4l2loopback.ko" ]; then
    echo "You need to build the loopback kernel module first! (see README.md)"
    exit 1
fi

if [ ! -d ".venv" ]; then
    echo "Initializing virtual environment!"
    source scripts/setup-venv.sh

    # Patch for python 3.9
    cp scripts/v4l2\ \(patch\).py .venv/lib/python3.9/site-packages/v4l2.py
fi

insmod v4l2loopback.ko \
    devices=1 exclusive_caps=1 video_nr=10 max_buffers=2 \
    card_label=v4l2lo

source .venv/bin/activate
python3.9 bgrm \
    $1 $2 $3 $4 $5 $6 $7 $8 $9 ${10} ${11} \
    ${12} ${13} ${14} ${15} ${16} ${17} ${18} ${19} ${20} ${21} ${22} \
    ${23} ${24} ${25}
deactivate

rmmod v4l2loopback
