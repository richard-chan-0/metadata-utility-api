from tkinter import *

import logging
from src.ffmpeg.ffmpeg_functions import *
from src.guis import return_gui

logger = logging.getLogger(__name__)


def main(utility_type):
    """main function for utility"""
    logger.info("retrieving service")
    gui = return_gui(utility_type)
    root = Tk()
    service = gui(root)
    service.start()


if __name__ == "__main__":
    main("ffmpeg")
