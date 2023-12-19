from tkinter import *
from src.data_types.media_types import *
from src.utilities.os_functions import create_sub_directory, parse_path
from src.tkinter.tkinter_functions import *
from src.ffmpeg.ffmpeg_functions import *
from typing import Iterable
from src.tkinter.gui import Gui
from src.exceptions.exceptions import ServiceError
from src.ffmpeg.ffmpeg_builder import FfmpegCommandBuilder
from src.data_types.DirectoryFile import DirectoryFile

from logging import getLogger

logger = getLogger(__name__)


class FfmpegGui(Gui):
    BLANK = "n/a"
    BACKGROUND_COLOR = "#141c15"
    DEFAULT_OPTIONS = {"bg": BACKGROUND_COLOR, "highlightbackground": BACKGROUND_COLOR}

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
        self.__root.configure(bg=self.BACKGROUND_COLOR)

    def __get_details_for_all_streams(self, language_streams: Iterable[Variable]):
        """function to go iterate over language streams and extract details"""
        all_language_stream_details = []
        for stream in language_streams:
            stream_number, stream_name, stream_language = get_language_widget_details(
                stream
            )
            if not stream_name and not stream_language:
                continue
            all_language_stream_details.append(
                (stream_number, stream_name, stream_language)
            )

        return all_language_stream_details

    def __set_default_streams(self):
        path = get_widget_value(self.__file_entry_text)
        audio_details = self.__get_details_for_all_streams(self.__default_audios)
        subtitle_details = self.__get_details_for_all_streams(self.__default_subtitles)
        audio_numbers = [audio_number for audio_number, _, _ in audio_details]

        subtitle_numbers = [
            subtitle_number for subtitle_number, _, _ in subtitle_details
        ]
        if not audio_numbers or not subtitle_numbers:
            self.log_to_console("no values selected for conversion!")
            return

        self.log_to_console("")
        files = get_files(path)
        if not files:
            return
        file = files[0]
        self.log_to_console(f"building command for file {file.name}", is_clear=False)
        command = build_command(
            file_path=file.path,
            audios=audio_numbers,
            subtitles=subtitle_numbers,
            attachment=None,
        )
        self.log_to_console(command, is_clear=False)
        self.__commands = [command]

    def __set_bulk_default_streams(self):
        path = get_widget_value(self.__file_entry_text)
        all_audio_details = self.__get_details_for_all_streams(self.__default_audios)
        all_subtitle_details = self.__get_details_for_all_streams(
            self.__default_subtitles
        )

        self.log_to_console("")
        files = get_files(path)

        if not files:
            return
        commands = []
        for file in files:
            self.log_to_console(
                f"building command for file {file.name}", is_clear=False
            )
            json_streams = get_media_streams(file.path)
            media_streams = parse_streams(json_streams)

            new_audio_numbers = get_matching_stream_numbers(
                "audio", all_audio_details, media_streams
            )
            new_subtitle_numbers = get_matching_stream_numbers(
                "subtitle", all_subtitle_details, media_streams
            )

            if not new_audio_numbers or not new_subtitle_numbers:
                self.log_to_console(
                    f"** could not find the language setting you are looking for {file.name}\n",
                    is_clear=False,
                )
                continue

            command = build_command(
                file_path=file.path,
                audios=new_audio_numbers,
                subtitles=new_subtitle_numbers,
                attachment=None,
            )
            self.log_to_console(command, is_clear=False)
            commands.append(command)

        self.__commands = commands

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
            options=self.DEFAULT_OPTIONS,
        )
        create_label(
            self.__root,
            "Audio Streams",
            self.__audio_dropdown_row,
            self.DEFAULT_OPTIONS,
        )
        default_audio, _ = create_dropdown(
            root=self.__audio_frame,
            options=self.__audio_list,
            row_position=0,
            column=0,
            command=lambda x: self.log_to_console(f"selected {x}"),
        )
        self.__setup_add_audio_button_image()
        create_image_buttoon(
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
            options=self.DEFAULT_OPTIONS,
        )
        create_label(
            self.__root,
            "Subtitle Streams",
            self.__subtitles_dropdown_row,
            self.DEFAULT_OPTIONS,
        )
        default_subtitle, _ = create_dropdown(
            root=self.__subtitle_frame,
            options=self.__subtitles_list,
            row_position=0,
            column=0,
            command=lambda x: self.log_to_console(f"selected {x}"),
        )
        self.__setup_add_subtitle_button_image()
        create_image_buttoon(
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
            self.DEFAULT_OPTIONS,
        )
        self.__default_attachment, _ = create_dropdown(
            self.__root,
            self.__attachments_list,
            self.__attachment_dropdown_row,
            lambda x: self.log_to_console(f"selected {x}"),
        )

    def __run_commands(self):
        is_okay = create_confirmation_window(
            "Confirmation", "Are you sure you want to run these commands?"
        )

        if not is_okay:
            self.log_to_console("ffmpeg aborted!")
            return

        for command in self.__commands:
            run_shell_command(command.get_command())

        self.log_to_console("completed default reset")

    def __create_buttons_component(self):
        frame = create_frame(
            self.__root, self.__buttons_component_row, 1, self.DEFAULT_OPTIONS
        )
        create_buttoon(
            root=frame,
            button_text="Set Defaults",
            action=self.__set_default_streams,
            row_position=0,
            col_position=0,
            options=self.DEFAULT_OPTIONS,
        )
        create_buttoon(
            root=frame,
            button_text="Set Bulk Defaults",
            action=self.__set_bulk_default_streams,
            row_position=0,
            col_position=1,
            options=self.DEFAULT_OPTIONS,
        )
        create_buttoon(
            root=frame,
            button_text="Run FFMPEG",
            action=self.__run_commands,
            row_position=0,
            col_position=2,
            options=self.DEFAULT_OPTIONS,
        )

    def inspect_files(self):
        """function to inspect files and save streams"""
        path = get_widget_value(self.__file_entry_text)
        try:
            streams = get_media_streams(path)
        except ServiceError as se:
            self.log_to_console(se)
            return

        stream_objs = parse_streams(streams)
        self.__subtitles_list = create_options(stream_objs.get("subtitle"))
        self.__audio_list = create_options(stream_objs.get("audio"))
        self.__attachments_list = create_options(stream_objs.get("attachment"))
        self.log_to_console(stream_objs)
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
            self.DEFAULT_OPTIONS,
        )
        self.__file_entry_text, _ = create_input_field(
            self.__root, self.__file_entry_row
        )
        create_buttoon(
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
        self.init_gui()
        self.__root.mainloop()
