# Background Remover

## The Need

It's been good long while since Microsoft first released a Teams version for Linux and yet, one of Teams' coolest features doesn't exist in said Linux version: removable backgrounds. As someone who uses Linux for their daily driver, this annoys me.

Well, I'm an engineer, so of course, I found a solution.

Using OpenCV and a v4l2loopback device (basically a virtual webcam you can write data to), I threw together a Python application that takes your normal webcam input, removes and replaces the background, and outputs that to the created video device. Problem solved :)

## How to Use

Take a video camera feed, process it to remove the background, apply a new one, and send it back as a loopback video device.

Buld the kernel module first with `make` (see dependency notes below!)

Run with `sudo ./bgrm.sh <options>`

Example: 
```
make ALT_BUILD_DIR=/tmp/bgrm
sudo ./bgrm.sh -b ~/Pictures/Wallpapers/ni-skyline-wallpaper.png -H 720
```

Note, this will work anywhere WebCams are used.

# Dependencies

Packages:
 - make
 - gcc
 - python3.9

The application is python based, but uses the [v4l2looopback](https://github.com/umlaeute/v4l2loopback) kernel module.

There's a makefile target to download and build that part. However, it must be built in a folder without spaces, so if you want to build it there, provide make a different directory to install to with `make ALT_BUILD_DIR=<folder name>`
