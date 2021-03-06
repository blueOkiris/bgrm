# Background Remover

## The Need

It's been good long while since Microsoft first released a Teams version for Linux and yet, one of Teams' coolest features doesn't exist in said Linux version: removable backgrounds. As someone who uses Linux for their daily driver, this annoys me.

Well, I'm an engineer, so of course, I found a solution.

Using OpenCV and a v4l2loopback device (basically a virtual webcam you can write data to), I threw together a Python application that takes your normal webcam input, removes and replaces the background, and outputs that to the created video device. Problem solved :)

Note, this will work anywhere WebCams are used, not just Teams

## How to Use

### Flatpak Installation:

Dependencies:
    - flatpak
    - flatpak-builder
    - v4l2loopback

1. Install - `flatpak-builder --install --user --force-clean build-dir com.blueokiris.bgrm.json`
2. Configure v4l2loopback (may not be necessary):
    - Recommended:
    ```
    export DEVICE_ARR=(`ls /sys/devices/virtual/video4linux | tr -d 'video'`); \
    sudo modprobe v4l2loopback \
        devices=1 exclusive_caps=1 video_nr=${DEVICE_ARR[1]} max_buffers=2 \
        card_label=v4l2lo
    ```
3. Run:
    - `flatpak run com.blueokiris.bgrm <options>` (use --help for options)
    - Example: `flatpak run com.blueokiris.bgrm -b ~/Pictures/Wallpapers/austin-apartment-backyard-bg.jpg -w 640 -H 480 -c 1`

### Manual Installation:

Dependencies:
    - python >= 3.9 (3.10 is what's supported officially)
    - pip
    - v4l2loopback

1. Setup (skip if installing via flatpak):
   - First time you set up you need to do the following (make sure you own the folder):
   - Create the proper virtual environment with `./scripts/setup-venv.sh`
   - Patch the v4l2 library `./scripts/patch-v4l2-py-mod.sh`
2. Configure v4l2loopback (may not be necessary):
    - Recommended:
    ```
    export DEVICE_ARR=(`ls /sys/devices/virtual/video4linux | tr -d 'video'`); \
    sudo modprobe v4l2loopback \
        devices=1 exclusive_caps=1 video_nr=${DEVICE_ARR[1]} max_buffers=2 \
        card_label=v4l2lo
    ```
3. Run:
   - Run with `./bgrm.sh <options>` (use `--help` to see all options)
   - Example: `./bgrm.sh -b ~/Pictures/Wallpapers/ni-skyline-wallpaper.png -w 320 -H 240 -s 2.0`

## Current State

As a package, this project has become relatively stable for me (considering it started as a little baby script just barely functioning), so I'm pretty much done use-case-wise. This was always a personal project intended for my own use, and it has reached the point where I can easily use it for daily use, so major features are probably done at this point.

So where to go now? The plan from here on out is just to help others to get the software running and possibly package it for other systems. If you'd like other features, then you're absolutely welcome to fork the project and make your own additions (I'll consider pull requests into this repo as well), but for now, I'm shifting gears to maintenance.

