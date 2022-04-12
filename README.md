# Background Remover

## The Need

It's been good long while since Microsoft first released a Teams version for Linux and yet, one of Teams' coolest features doesn't exist in said Linux version: removable backgrounds. As someone who uses Linux for their daily driver, this annoys me.

Well, I'm an engineer, so of course, I found a solution.

Using OpenCV and a v4l2loopback device (basically a virtual webcam you can write data to), I threw together a Python application that takes your normal webcam input, removes and replaces the background, and outputs that to the created video device. Problem solved :)

## How to Use

__Setup:__
1. Install dependencies
2. Build with `cargo build --release`. The binary will be in target/release/bgrm
3. Move it to /usr/bin

__Running:__

Either:

`sudo bgrm <options>` (use `--help` to see all the options)
  - Example: `sudo bgrm -b ~/Pictures/Wallpapers/wallpaper.png -w 320 -H 240 -s 2.0`

Or, if you don't want to use sudo everytime, manually set up the v4l2looback module (there's a way to make it permanent):

```
modprobe v4l2loopback \
   devices=1 exclusive_caps=1 video_nr=10 max_buffers=2 \
   card_label=v4l2lo
```

And then run like before, but without sudo

__Dependencies:__

Non-Python dependencies:
- Linux
- cargo
- v4l2loopback-dkms
- opencv4
- ffmpeg
- bazel
- mediapipe C++ lib (there's no package for this :/)
  1. `git clone https://github.com/google/mediapipe.git` (takes a long time)
  2. `cd mediapipe`
  3. Modify third_party/opencv_linux.BUILD to specify x86_64-linux-gnu (uncomment lines 20 and 27)
  4. Modify .bazelversion to match your bazel (mine was at 5.1.0 while the project required 5.0.0)
  5. Set your openjdk-11 java home (java is not a direct dependency, but it is a dependency for bazel). For me that's `export JAVA_HOME=/usr/lib/jvm/java-11-openjdk/`
  6. ``
  7. Copy to /usr/share/lib
    - 
