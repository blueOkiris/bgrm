#!/usr/bin/env python3

# Author: Dylan Turner
# Description: Main loop for bgrm app

from numpy import shape
from bgrm.cam import Cam
from bgrm.virt_cam import VirtCam
from bgrm.vid_file import VidFile
from bgrm.settings import AppSettings

def main():
    settings = AppSettings.from_cli()

    if not settings.file_mode:
        virt_dev_name = '/dev/video' + str(settings.virt_dev)
        with Cam(settings) as cam, VirtCam(virt_dev_name) as virt_cam:
            virt_cam.format(cam, settings)
            while True:
                _frame, no_bg_frame, stacked_frames = cam.frames()
                virt_cam.write(no_bg_frame)

                if not cam.display(stacked_frames):
                    break
    else:
        with VidFile(settings) as vid_file:
            while True:
                frame, no_bg_frame, stacked_frames = vid_file.frames()

                if shape(frame) == ():
                    break

                vid_file.write(no_bg_frame)
                
                if not vid_file.display(stacked_frames):
                    break

