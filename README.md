# Background Remover

## The Need

It's been good long while since Microsoft first released a Teams version for Linux and yet, one of Teams' coolest features doesn't exist in said Linux version: removable backgrounds. As someone who uses Linux for their daily driver, this annoys me.

Well, I'm an engineer, so of course, I found a solution.

Using OpenCV and a v4l2loopback device (basically a virtual webcam you can write data to), I threw together a Python application that takes your normal webcam input, removes and replaces the background, and outputs that to the created video device. Problem solved :)

## How to Use

__Setup:__
1. Install dependencies
2. Build with `cargo build --release`. The binary will be in target/release/bgrm
3. Move it to /bin
4. Run `pip install --user virtualenv`
5. Create a python virtualenv in \~/.bgrm/ with `mkdir ~/.bgrm; cd ~/.bgrm; virtualenv .venv`
6. Source the virtualenv with `source ~/.bgrm/.venv/bin/activate`
7. Run `pip install cvzone`
8. Run `deactivate`

__Running:__
`sudo bgrm <options>` (use `--help` to see all the options)
  - Example: `sudo bgrm -b ~/Pictures/Wallpapers/wallpaper.png -w 320 -H 240 -s 2.0`

__Dependencies:__

Non-Python dependencies:
- Linux
- cargo
- v4l2loopback-dkms
- opencv
- python > 3.6
- python3-pip (to install deps)

Python Dependencies (i.e. pip):
- virtualenv
- cvzone >= 1.5.6 (requires Python > 3.6)

##

 - python >= 3.9
 - pip
 - v4l2loopback-dkms


$$

1. Setup
   - First time you set up you need to do the following
   - Create the proper virtual environment with `./scripts/setup-env.sh`
   - Patch the v4l2 library `./scripts/patch-v4l2-py-mod.sh`

2. Run
   - After setting up, you can run the application
   - Run with `sudo ./bgrm.sh <options>` (use `--help` to see all options)
   - Example: `sudo ./bgrm.sh -b ~/Pictures/Wallpapers/ni-skyline-wallpaper.png -w 320 -H 240 -s 2.0`

Note, this will work anywhere WebCams are used.
