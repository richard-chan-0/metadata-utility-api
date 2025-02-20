from tkinter import *

import logging
from src.ffmpeg.ffmpeg_functions import *
from src.tkinter.ffmpeg_gui import FfmpegGui

logger = logging.getLogger(__name__)


def main():
    """main function for utility"""
    gui = FfmpegGui
    root = Tk()
    service = gui(root)
    service.start()


if __name__ == "__main__":
    main()
