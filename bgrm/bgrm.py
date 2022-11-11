#!/usr/bin/env python3

# Author: Dylan Turner
# Description: Main loop for bgrm app

from cv2 import cvtColor, COLOR_BGR2YUV_I420
from v4l2 import \
    v4l2_format, V4L2_BUF_TYPE_VIDEO_OUTPUT, V4L2_FIELD_NONE, \
    V4L2_PIX_FMT_YUV420, VIDIOC_S_FMT
from fcntl import ioctl

from bgrm.cam import Cam
from bgrm.settings import AppSettings

def main():
    settings = AppSettings.from_cli()

    with Cam(settings) as cam, open('/dev/video' + str(settings.virt_dev), 'wb') as virtCam:
        formatVirtualCamera(settings, virtCam, cam)

        # Loop over feed
        while True:
            # Get cam feed
            frame, no_bg_frame, stacked_frames = cam.frames()

            # Write to virtual camera
            virtCam.write(cvtColor(no_bg_frame, COLOR_BGR2YUV_I420))

            # Display
            if not cam.display(stacked_frames):
                break

def formatVirtualCamera(settings, virtCam, actualCam):
    # Setup format info for writing to cam device
    format = v4l2_format()
    format.type = V4L2_BUF_TYPE_VIDEO_OUTPUT
    format.fmt.pix.field = V4L2_FIELD_NONE
    format.fmt.pix.pixelformat = V4L2_PIX_FMT_YUV420
    format.fmt.pix.width = settings.screen_width
    format.fmt.pix.height = settings.screen_height
    format.fmt.pix.bytesperline = settings.screen_width * actualCam.channels
    format.fmt.pix.sizeimage = \
        settings.screen_width * settings.screen_height * actualCam.channels
    
    # Set device format
    print('Format loopback format result (0 good): {}'.format(
        ioctl(virtCam, VIDIOC_S_FMT, format)
    ))

