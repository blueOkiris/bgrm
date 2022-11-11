# Author: Dylan Turner
# Description: Handle OpenCV processing of images

from cv2 import \
    VideoCapture, resize, namedWindow, moveWindow, imshow, waitKey, \
    destroyAllWindows, imread
from numpy import shape
from cvzone import stackImages
from cvzone.SelfiSegmentationModule import SelfiSegmentation
from time import sleep

WIN_TITLE = 'Feed'

class Cam:
    def __init__(self, settings):
        self._settings = settings

        self._vidFeed = VideoCapture(settings.camera)
        self._vidFeed.set(3, settings.screen_width)
        self._vidFeed.set(4, settings.screen_height)

        self._segmentor = SelfiSegmentation()

        _success, baseFrame = self._vidFeed.read()
        if not _success:
            print('Failed to read from camera!')
            quit()
        _height, _width, self.channels = baseFrame.shape

        if not settings.disable_win:
            namedWindow(WIN_TITLE)
    
    def __enter__(self):
        return self
    
    def getFrame(self, bgImg = None):
        _success, frame = self._vidFeed.read()

        if shape(bgImg) == ():
            noBgFrame = self._segmentor.removeBG(
                frame, self._settings.fill_color,
                threshold = self._settings.rm_thresh
            )
        else:
            noBgFrame = self._segmentor.removeBG(
                frame, bgImg,
                threshold = self._settings.rm_thresh
            )
        return (frame, noBgFrame)
    
    def stackFrames(self, leftFrame, rightFrame):
        newWidth = int(self._settings.screen_width * self._settings.view_scale)
        newHeight = int(self._settings.screen_height * self._settings.view_scale)
        return stackImages(
            [
                resize(leftFrame, (newWidth, newHeight)),
                resize(rightFrame, (newWidth, newHeight))
            ], 1, 1
        )
    
    def display(self, frame):
        if not self._settings.disable_win:
            imshow(WIN_TITLE, frame)

        if waitKey(1) & 0xFF == ord('q'):
            return False
        return True
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._vidFeed.release()
        destroyAllWindows()
