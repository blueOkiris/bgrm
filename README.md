# Background Remover

## The Need

It's been good long while since Microsoft first released a Teams version for Linux and yet, one of Teams' coolest features doesn't exist in said Linux version: removable backgrounds. As someone who uses Linux for their daily driver, this annoys me.

Well, I'm an engineer, so of course, I found a solution.

Using OpenCV and a v4l2loopback device (basically a virtual webcam you can write data to), I threw together a Python application that takes your normal webcam input, removes and replaces the background, and outputs that to the created video device. Problem solved :)

Note, this will work anywhere WebCams are used, not just Teams

Now, the program can also be used to remove backgrounds from video files and save them as video files as well!

## How to Use

### WebCam Replacement

Dependencies:
    - python >= 3.8 (3.10 is what's supported officially)
    - pip
    - v4l2loopback

Setup:
1. Configure v4l2loopback (may not be necessary):
    - Recommended something like this:
    ```
    export DEVICE_ARR=(`ls /sys/devices/virtual/video4linux | tr -d 'video'`); \
    sudo modprobe v4l2loopback \
        devices=1 exclusive_caps=1 video_nr=${DEVICE_ARR[1]} max_buffers=2 \
        card_label=v4l2lo
    ```
2. Install with `pip install bgrm`

Then, you can run: 
- Run with `python -m bgrm <options>` (use `--help` to see all options)
- Example: `python -m bgrm -b ~/Pictures/Wallpapers/ni-skyline-wallpaper.png -w 320 -H 240 -s 2.0`

### File Replacement

You can also remove the background from video files. It works just like the WebCam, but instead of setting the `--camera` cli arg, you call the program like this:

`python -m bgrm --file_mode -i <input file> -o <output file> <other options>`

## Build from Repo

You can also build the package yourself from source (or grab the latest version from the releases tab)

To do that you need the "poetry" build system.

Run `poetry build` and install the whl from the dist/ folder
