# Author: Dylan Turner
# Description: Encapsulate code to format and write to virtual camera device

from cv2 import cvtColor, COLOR_BGR2YUV_I420
from v4l2 import \
        v4l2_format, V4L2_BUF_TYPE_VIDEO_OUTPUT, V4L2_FIELD_NONE, \
    V4L2_PIX_FMT_YUV420, VIDIOC_S_FMT
from fcntl import ioctl

class VirtCam:
    def __init__(self, dev_name):
        self._device = open(dev_name, 'wb')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._device.close()

    def write(self, frame):
        self._device.write(cvtColor(frame, COLOR_BGR2YUV_I420))

    def format(self, actual_cam, settings):
        # Setup format info for writing to cam device
        fmt = v4l2_format()
        fmt.type = V4L2_BUF_TYPE_VIDEO_OUTPUT
        fmt.fmt.pix.field = V4L2_FIELD_NONE
        fmt.fmt.pix.pixelformat = V4L2_PIX_FMT_YUV420
        fmt.fmt.pix.width = settings.screen_width
        fmt.fmt.pix.height = settings.screen_height
        fmt.fmt.pix.bytesperline = settings.screen_width * actual_cam.channels
        fmt.fmt.pix.sizeimage = \
            settings.screen_width * settings.screen_height * actual_cam.channels

        # Set device format
        print('Format loopback format result (0 good): {}'.format(
            ioctl(self._device, VIDIOC_S_FMT, fmt)
        ))

