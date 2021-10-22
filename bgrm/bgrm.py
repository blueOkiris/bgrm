#!/usr/bin/env python3

# Force a version of OpenCV that works (not all do)
import pkg_resources
pkg_resources.require("opencv-python<=4.4.0.46")

from cv2 import imread, resize, copyMakeBorder, BORDER_CONSTANT
from v4l2 import \
    v4l2_format, V4L2_BUF_TYPE_VIDEO_OUTPUT, V4L2_FIELD_NONE, \
    V4L2_PIX_FMT_BGR24, VIDIOC_S_FMT
from fcntl import ioctl

from cam import Cam
from settings import AppSettings

def main():
    settings = AppSettings.fromArguments()

    # Setup a background image to plug into the cam functions
    if settings.bgImg != '':
        bgImg = getCorrectlySizedBg(settings)
    
    with Cam(settings) as cam, open('/dev/video10', 'wb') as virtCam:
        # Setup format info for writing to cam device
        format = v4l2_format()
        format.type = V4L2_BUF_TYPE_VIDEO_OUTPUT
        format.fmt.pix.field = V4L2_FIELD_NONE
        format.fmt.pix.pixelformat = V4L2_PIX_FMT_BGR24
        format.fmt.pix.width = settings.screenWidth
        format.fmt.pix.height = settings.screenHeight
        format.fmt.pix.bytesperline = settings.screenWidth * cam.channels
        format.fmt.pix.sizeimage = \
            settings.screenWidth * settings.screenHeight * cam.channels
        
        # Set device format
        print('Format loopback format result (0 good): {}'.format(
            ioctl(virtCam, VIDIOC_S_FMT, format)
        ))

        # Loop over feed
        while True:
            # Get cam feed
            if settings.bgImg == '':
                frame, noBgFrame = cam.getFrame()
            else:
                frame, noBgFrame = cam.getFrame(bgImg)
            
            # Write to virtual camera
            virtCam.write(noBgFrame)

            # Display
            stackFrame = cam.stackFrames(frame, noBgFrame)
            if not cam.display(stackFrame):
                break

def getCorrectlySizedBg(settings):
    bgImg = imread(settings.bgImg)

    # Scale to match y and be centered
    bgHeight, bgWidth, _channels = bgImg.shape
    aspect = float(bgWidth) / float(bgHeight)
    newWidth = int(settings.screenHeight * aspect)
    bgImg = resize(bgImg, (newWidth, settings.screenHeight))

    # Scale down
    if newWidth > settings.screenWidth:
        startx = int((newWidth - settings.screenWidth) / 2)
        endx = newWidth - startx
        bgImg = bgImg[0:settings.screenHeight, startx:endx]
    else:
        padding = int((settings.screenWidth - newWidth) / 2)
        bgImg = copyMakeBorder(
            bgImg, 0, 0, padding, padding, BORDER_CONSTANT
        )
    
    # Make sure correct size
    bgImg = resize(bgImg, (settings.screenWidth, settings.screenHeight))
    return bgImg
