# Author: Dylan Turner
# Description: Handle OpenCV processing of images

from cv2 import \
    VideoCapture, resize, namedWindow, moveWindow, imshow, waitKey, \
    destroyAllWindows, imread, BORDER_CONSTANT, copyMakeBorder, resize, imread, \
    GaussianBlur
from numpy import shape, uint8
from cvzone import stackImages
from cvzone.SelfiSegmentationModule import SelfiSegmentation
from time import sleep

WIN_TITLE = 'Feed'

class Cam:
    def __init__(self, settings):
        # Set up WebCam access and output
        self._settings = settings

        self._vid_feed = VideoCapture(settings.camera)
        self._vid_feed.set(3, settings.screen_width)
        self._vid_feed.set(4, settings.screen_height)

        _success, baseFrame = self._vid_feed.read()
        if not _success:
            print('Failed to read from camera!')
            quit()
        _height, _width, self.channels = baseFrame.shape

        if not settings.disable_win:
            namedWindow(WIN_TITLE)

        # Set up removal
        self._segmentor = SelfiSegmentation()

        if settings.bg_img != '':
            self._bg_img = self._create_correctly_sized_bg()
        else:
            self._bg_img = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._vid_feed.release()
        destroyAllWindows()

    # Return regular camera frame and with the bg removal applied, as well as them put together
    def frames(self):
        success, frame = self._vid_feed.read()

        if not success:
            return (None, None, None)

        if shape(self._bg_img) == ():
            no_bg_frame = self._segmentor.removeBG(
                frame, self._settings.fill_color,
                threshold = self._settings.rm_thresh
            )
        else:
            no_bg_frame = self._segmentor.removeBG(
                frame, self._bg_img,
                threshold = self._settings.rm_thresh
            )

        if self._settings.blur:
            removed_bg = frame - no_bg_frame
            blurred = GaussianBlur(removed_bg, (77, 77), 21)
            no_bg_frame += blurred

        return (frame, no_bg_frame, self._stack_frames(frame, no_bg_frame))

    def display(self, frame):
        if not self._settings.disable_win:
            imshow(WIN_TITLE, frame)

        if waitKey(1) & 0xFF == ord('q'):
            return False

        return True

    def _stack_frames(self, left_frame, right_frame):
        new_width = int(self._settings.screen_width * self._settings.view_scale)
        new_height = int(self._settings.screen_height * self._settings.view_scale)
        return stackImages(
            [
                resize(left_frame, (new_width, new_height)),
                resize(right_frame, (new_width, new_height))
            ], 1, 1
        )

    # Adjust self._bg_img to be the size we want
    def _create_correctly_sized_bg(self):
        bg_img = imread(self._settings.bg_img)

        # Scale to match y and be centered
        bg_height, bg_width, _channels = bg_img.shape
        aspect = float(bg_width) / float(bg_height)
        new_width = int(self._settings.screen_height * aspect)
        bg_img = resize(bg_img, (new_width, self._settings.screen_height))

        # Scale down
        if new_width > self._settings.screen_width:
            startx = int((new_width - self._settings.screen_width) / 2)
            endx = new_width - startx
            bg_img = bg_img[0:self._settings.screen_height, startx:endx]
        else:
            padding = int((self._settings.screen_width - new_width) / 2)
            bg_img = copyMakeBorder(bg_img, 0, 0, padding, padding, BORDER_CONSTANT)

        # Make sure correct size
        bg_img = resize(bg_img, (self._settings.screen_width, self._settings.screen_height))

        return bg_img

