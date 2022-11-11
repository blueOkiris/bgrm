# Author: Dylan Turner
# Description: File-to-file version of Cam class

from cv2 import VideoCapture, VideoWriter, VideoWriter_fourcc, namedWindow, destroyAllWindows
from cvzone.SelfiSegmentationModule import SelfiSegmentation
from bgrm.cam import Cam

WIN_TITLE = 'Conversion'

class VidFile(Cam):
    def __init__(self, settings):
        self._settings = settings

        # Set up file input
        self._vid_feed = VideoCapture(settings.input_file)
        _success, base_frame = self._vid_feed.read()
        height, width, self.channels = base_frame.shape
        self._settings.screen_width = width
        self._settings.screen_height = height
        settings.screen_width = width
        settings.screen_height = height

        if not settings.disable_win:
            namedWindow(WIN_TITLE)

        # Set up removal
        self._segmentor = SelfiSegmentation()

        if settings.bg_img != '':
            self._bg_img = self._create_correctly_sized_bg()
        else:
            self._bg_img = None

        # Set up file output
        self._out_feed = VideoWriter(
            settings.output_file, VideoWriter_fourcc('M', 'J', 'P', 'G'),
            settings.fps, (width, height)
        )

    def __exit__(self, exc_type, exc_value, traceback):
        self._vid_feed.release()
        self._out_feed.release()
        destroyAllWindows() 

    def write(self, frame):
        self._out_feed.write(frame)

