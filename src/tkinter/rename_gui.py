from tkinter import *
from src.services import (
    return_service,
)
from src.exceptions.exceptions import ServiceError
from src.utilities.os_functions import transfer_files
from src.tkinter.tkinter_functions import *
from src.tkinter.gui import Gui

from logging import getLogger

logger = getLogger(__name__)


class RenameGui(Gui):
    BACKGROUND_COLOR = "#101010"
    DEFAULT_OPTIONS = {"bg": BACKGROUND_COLOR, "highlightbackground": BACKGROUND_COLOR}

    def __init__(self, root: Tk):
        self.__root = root

        self.directory_in = None
        self.directory_out = None
        self.service = None
        self.__download_entry_row = 1
        self.__service_message_row = 100

        self.__service_message = None

        self.__download_text = None

    def __create_window(self):
        width = 900
        height = 450
        dimension = f"{width}x{height}"
        self.__root.geometry(dimension)
        self.__root.configure(bg=self.BACKGROUND_COLOR)

    def __configure_service(self, service_name: str):
        logger.info("configuring utility...")
        service_metadata = return_service(service_name)
        self.directory_in = service_metadata.directory_in
        self.directory_out = service_metadata.directory_out
        self.service = service_metadata.service

    def init_gui(self, value: str):
        """function to add widgets based on service selected"""
        logger.info("adding download widget to window")
        self.__create_console_message()
        self.log_to_console(f"setting up {value} service")
        self.__configure_service(value)

        self.__create_download_files_entry()

    def pull_files_from_download(self):
        download_path = get_widget_value(self.__download_text)
        if not download_path or not self.directory_in:
            self.log_to_console("no download directory or destination directory set")
            return

        try:
            transfer_files(download_path, self.directory_in)
            self.log_to_console("files have been pulled!")
        except ServiceError as err:
            self.log_to_console(str(err))

    def __create_download_files_entry(self):
        """function to setup entry component for entering path of download folder"""
        create_label(
            self.__root,
            "Download Directory:",
            row=self.__download_entry_row,
            options=self.DEFAULT_OPTIONS,
        )

        text, _ = create_input_field(self.__root, self.__download_entry_row)
        self.__download_text = text

    def log_to_console(self, message: str):
        """function to update the console window in gui to message"""
        self.__service_message.configure(state="normal")
        self.__service_message.delete(1.0, END)
        self.__service_message.insert(INSERT, message)
        self.__service_message.configure(state="disabled")

    def __create_console_message(self):
        """function to create the console window on gui"""
        create_label(
            self.__root,
            text="Console",
            row=self.__service_message_row,
            options=self.DEFAULT_OPTIONS,
        )

        options = {
            "background": "black",
            "width": "100",
            "height": "20",
        }
        self.__service_message = create_console_textbox(
            self.__root,
            options=options,
            row=self.__service_message_row,
            col=1,
        )

    def start(self):
        self.__create_window()
        self.__root.mainloop()
