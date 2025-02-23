from tkinter import *
from src.data_types.media_types import *
from src.tkinter.tkinter_functions import *
from src.ffmpeg.ffmpeg_functions import *
from typing import Iterable
from src.tkinter.gui import Gui
from src.tkinter.functions.actions import (
    set_streams,
    run_ffmpeg,
    set_bulk_commands,
    set_single_command,
)
from dataclasses import dataclass
from src.tkinter.functions.actions import (
    set_streams,
    run_ffmpeg,
    set_bulk_commands,
    set_single_command,
)
from dataclasses import dataclass

from logging import getLogger

logger = getLogger(__name__)

BLANK = "n/a"
BACKGROUND_COLOR = "#141c15"
DEFAULT_OPTIONS = {"bg": BACKGROUND_COLOR, "highlightbackground": BACKGROUND_COLOR}


@dataclass
class ButtonDetails:
    button_text: str
    action: Callable


class FfmpegGui(Gui):

    def __init__(self, root: Tk):
        self.__root = root
        self.__root.title("FFMPEG Default Changer")
        self.__add_subtitle_button_image = None
        self.__add_audio_button_image = None

        self.__file_entry_row = 0
        self.__inspect_file_button_row = 1
        self.__subtitles_dropdown_row = 3
        self.__audio_dropdown_row = 2
        self.__attachment_dropdown_row = 4
        self.__buttons_component_row = 50

        self.__service_message_row = 100

        self.__file_entry_text = None
        self.__default_attachment = None
        self.__default_audios = []
        self.__default_subtitles = []

        self.__service_message = None
        self.__subtitle_frame = None
        self.__subtitles_list = []
        self.__num_subtitle_dropdowns = 0

        self.__audio_frame = None
        self.__num_audio_dropdowns = 0
        self.__audio_list = []

        self.__attachments_list = []
        self.__commands = []

    def __setup_add_subtitle_button_image(self):
        my_img = create_photoimage("resources/add_button.jpg", (20, 20))
        self.__add_subtitle_button_image = my_img

    def __setup_add_audio_button_image(self):
        my_img = create_photoimage("resources/add_button.jpg", (20, 20))
        self.__add_audio_button_image = my_img

    def __create_window(self):
        width = 900
        height = 450
        dimension = f"{width}x{height}"
        self.__root.geometry(dimension)
        self.__root.configure(bg=BACKGROUND_COLOR)

    def __set_default_streams(self):
        self.__commands = set_single_command(
            self.log_to_console,
            self.__file_entry_text,
            self.__default_audios,
            self.__default_subtitles,
        )

    def __set_bulk_default_streams(self):
        self.__commands = set_bulk_commands(
            self.__file_entry_text,
            self.__default_audios,
            self.__default_subtitles,
            self.log_to_console,
        )

    def __add_extra_audio_dropdown(self):
        if self.__num_audio_dropdowns == 3:
            self.log_to_console("no more audios can be added")
            return
        self.__num_audio_dropdowns += 1
        default_audio, _ = create_dropdown(
            root=self.__audio_frame,
            options=self.__audio_list,
            row_position=self.__num_audio_dropdowns,
            column=0,
            command=lambda x: self.log_to_console(f"selected {x}"),
        )
        self.__default_audios.append(default_audio)

    def __add_audio_component(self):
        self.__audio_frame = create_frame(
            root=self.__root,
            row=self.__audio_dropdown_row,
            column=1,
            options=DEFAULT_OPTIONS,
        )
        create_label(
            self.__root,
            "Audio Streams",
            self.__audio_dropdown_row,
            DEFAULT_OPTIONS,
        )
        default_audio, _ = create_dropdown(
            root=self.__audio_frame,
            options=self.__audio_list,
            row_position=0,
            column=0,
            command=lambda x: self.log_to_console(f"selected {x}"),
        )
        self.__setup_add_audio_button_image()

        create_image_button(
            self.__audio_frame,
            self.__add_audio_button_image,
            row_position=0,
            col_position=1,
            command=self.__add_extra_audio_dropdown,
        )
        self.__default_audios.append(default_audio)

    def __add_extra_subtitle_dropdown(self):
        if self.__num_subtitle_dropdowns == 3:
            self.log_to_console("no more subtitles can be added")
            return
        self.__num_subtitle_dropdowns += 1
        default_subtitle, _ = create_dropdown(
            root=self.__subtitle_frame,
            options=self.__subtitles_list,
            row_position=self.__num_subtitle_dropdowns,
            column=0,
            command=lambda x: self.log_to_console(f"selected {x}"),
        )
        self.__default_subtitles.append(default_subtitle)

    def __add_subtitle_component(self):
        self.__subtitle_frame = create_frame(
            root=self.__root,
            row=self.__subtitles_dropdown_row,
            column=1,
            options=DEFAULT_OPTIONS,
        )
        create_label(
            self.__root,
            "Subtitle Streams",
            self.__subtitles_dropdown_row,
            DEFAULT_OPTIONS,
        )
        default_subtitle, _ = create_dropdown(
            root=self.__subtitle_frame,
            options=self.__subtitles_list,
            row_position=0,
            column=0,
            command=lambda x: self.log_to_console(f"selected {x}"),
        )
        self.__setup_add_subtitle_button_image()
        create_image_button(
            self.__subtitle_frame,
            self.__add_subtitle_button_image,
            row_position=0,
            col_position=1,
            command=self.__add_extra_subtitle_dropdown,
        )
        self.__default_subtitles.append(default_subtitle)

    def __add_attachments_component(self):
        create_label(
            self.__root,
            "Attachments",
            self.__attachment_dropdown_row,
            DEFAULT_OPTIONS,
        )
        self.__default_attachment, _ = create_dropdown(
            self.__root,
            self.__attachments_list,
            self.__attachment_dropdown_row,
            lambda x: self.log_to_console(f"selected {x}"),
        )

    def __run_commands(self):
        run_ffmpeg(self.__commands, self.log_to_console)

    def __create_buttons_component(self):
        frame = create_frame(
            self.__root, self.__buttons_component_row, 1, DEFAULT_OPTIONS
        )

        button_details = [
            ButtonDetails("Set Defaults", self.__set_default_streams),
            ButtonDetails("Set Bulk Defaults", self.__set_bulk_default_streams),
            ButtonDetails("Run FFMPEG", self.__run_commands),
        ]

        for col, button in enumerate(button_details):
            create_button(
                root=frame,
                button_text=button.button_text,
                action=button.action,
                row_position=0,
                col_position=col,
                options=DEFAULT_OPTIONS,
            )

    def inspect_files(self):
        """function to inspect files and save streams"""
        streams = set_streams(self.__file_entry_text, self.log_to_console)
        self.__subtitles_list = streams.get("subtitles")
        self.__audio_list = streams.get("audio")
        self.__attachments_list = streams.get("attachments")

        self.__add_audio_component()
        self.__add_subtitle_component()
        # self.__add_attachments_component()
        self.__create_buttons_component()

    def init_gui(self):
        """function to initialize the gui"""
        logger.info("configuring menu")

        create_label(
            self.__root,
            "Enter a File/Directory",
            self.__file_entry_row,
            DEFAULT_OPTIONS,
        )
        self.__file_entry_text, _ = create_input_field(
            self.__root, self.__file_entry_row
        )

        create_button(
            self.__root,
            "Inspect File(s)",
            self.inspect_files,
            self.__inspect_file_button_row,
            1,
        )

        self.__create_console_message()

    def log_to_console(self, message, is_clear: bool = True):
        """function to update the console window in gui to message"""
        self.__service_message.configure(state="normal")
        if is_clear:
            self.__service_message.delete(1.0, END)
        self.__service_message.insert(INSERT, f"{message}\n")
        self.__service_message.configure(state="disabled")

    def __create_console_message(self):
        """function to create the console window on gui"""
        create_label(
            self.__root,
            text="Console",
            row=self.__service_message_row,
            options=DEFAULT_OPTIONS,
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
        self.init_gui()
        self.__root.mainloop()
