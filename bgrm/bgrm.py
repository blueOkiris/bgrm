#!/usr/bin/env python3

# Author: Dylan Turner
# Description: Main loop for bgrm app

from cv2 import \
    GaussianBlur, imread, resize, copyMakeBorder, \
    BORDER_CONSTANT, cvtColor, COLOR_BGR2YUV_I420
from v4l2 import \
    v4l2_format, V4L2_BUF_TYPE_VIDEO_OUTPUT, V4L2_FIELD_NONE, \
    V4L2_PIX_FMT_YUV420, VIDIOC_S_FMT
from fcntl import ioctl

from bgrm.cam import Cam
from bgrm.settings import AppSettings

WIN_TITLE = 'Feed'

def main():
    settings = AppSettings.from_cli()

    # Setup a background image to plug into the cam functions
    if settings.bg_img != '':
        bgImg = getCorrectlySizedBg(settings)

    with Cam(settings) as cam, open('/dev/video' + str(settings.virt_dev), 'wb') as virtCam:
        formatVirtualCamera(settings, virtCam, cam)

        # Loop over feed
        while True:
            # Get cam feed
            if not settings.blur and settings.bg_img != '':
                frame, noBgFrame = cam.getFrame(bgImg)
            else:
                frame, noBgFrame = cam.getFrame()
            
            # If blur enabled, then reapply the background, but blurrd
            if settings.blur:
                removedBg = frame - noBgFrame
                blurred = GaussianBlur(removedBg, (77, 77), 21)
                noBgFrame += blurred
            
            # Write to virtual camera
            virtCam.write(cvtColor(noBgFrame, COLOR_BGR2YUV_I420))
            
            # Display
            stackFrame = cam.stackFrames(frame, noBgFrame)
            if not cam.display(stackFrame):
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

def getCorrectlySizedBg(settings):
    bgImg = imread(settings.bg_img)

    # Scale to match y and be centered
    bgHeight, bgWidth, _channels = bgImg.shape
    aspect = float(bgWidth) / float(bgHeight)
    newWidth = int(settings.screen_height * aspect)
    bgImg = resize(bgImg, (newWidth, settings.screen_height))

    # Scale down
    if newWidth > settings.screen_width:
        startx = int((newWidth - settings.screen_width) / 2)
        endx = newWidth - startx
        bgImg = bgImg[0:settings.screen_height, startx:endx]
    else:
        padding = int((settings.screen_width - newWidth) / 2)
        bgImg = copyMakeBorder(
            bgImg, 0, 0, padding, padding, BORDER_CONSTANT
        )
    
    # Make sure correct size
    bgImg = resize(bgImg, (settings.screen_width, settings.screen_height))
    return bgImg
