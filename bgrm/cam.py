# Author: Dylan Turner
# Description: Handle OpenCV processing of images

from cv2 import \
    VideoCapture, resize, namedWindow, moveWindow, imshow, waitKey, \
    destroyAllWindows, imread
from cvzone import stackImages
from cvzone.SelfiSegmentationModule import SelfiSegmentation

class Cam:
    def __init__(self, settings):
        self._settings = settings

        self._vidFeed = VideoCapture(settings.camera)
        self._vidFeed.set(3, settings.screenWidth)
        self._vidFeed.set(4, settings.screenHeight)

        self._segmentor = SelfiSegmentation()

        _success, baseFrame = self._vidFeed.read()
        _height, _width, self.channels = baseFrame.shape
    
    def __enter__(self):
        return self
    
    def getFrame(self):
        _success, frame = self._vidFeed.read()
        noBgFrame = self._segmentor.removeBG(
            frame, self._settings.fillColor,
            threshold = self._settings.rmThresh
        )
        return (frame, noBgFrame)
    
    def getFrame(self, bgImg):
        _success, frame = self._vidFeed.read()
        noBgFrame = self._segmentor.removeBG(
            frame, bgImg,
            threshold = self._settings.rmThresh
        )
        return (frame, noBgFrame)
    
    def stackFrames(self, leftFrame, rightFrame):
        newWidth = int(self._settings.screenWidth * self._settings.viewScale)
        newHeight = int(self._settings.screenHeight * self._settings.viewScale)
        return stackImages(
            [
                resize(leftFrame, (newWidth, newHeight)),
                resize(rightFrame, (newWidth, newHeight))
            ], 1, 1
        )
    
    def display(self, frame):
        namedWindow(self._settings.winTitle)
        moveWindow(
            self._settings.winTitle,
            self._settings.winStartX, self._settings.winStartY
        )
        imshow(self._settings.winTitle, frame)

        if waitKey(1) & 0xFF == self._settings.quitKey:
            return False
        return True
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._vidFeed.release()
        destroyAllWindows()
