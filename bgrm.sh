#!/bin/bash

# Author: Dylan Turner
# Description: Run everything

if [ $(id -u) != "0" ]; then
    echo "You need to be root to run bgrm!"
    exit 1
fi

export DEVICE_ARR=(`ls /sys/devices/virtual/video4linux | tr -d 'video'`)

echo "Using device /dev/video${DEVICE_ARR[0]}"
modprobe v4l2loopback \
    devices=1 exclusive_caps=1 video_nr=${DEVICE_ARR[1]} max_buffers=2 \
    card_label=v4l2lo

source .venv/bin/activate
python bgrm \
    ${DEVICE_ARR[0]} $1 $2 $3 $4 $5 $6 $7 $8 $9 ${10} ${11} \
    ${12} ${13} ${14} ${15} ${16} ${17} ${18} ${19} ${20} ${21} ${22} \
    ${23} ${24} ${25} ${26}
deactivate

