from tkinter import *
from src.data_types.media_types import *
from src.utilities.os_functions import create_sub_directory, parse_path
from src.tkinter.tkinter_functions import *
from src.ffmpeg.ffmpeg_functions import *
from typing import Iterable
from src.tkinter.gui import Gui
from src.exceptions.exceptions import ServiceError
from src.ffmpeg.ffmpeg_builder import FfmpegCommandBuilder

from logging import getLogger

logger = getLogger(__name__)


class FfmpegGui(Gui):
    BLANK = "n/a"
    BACKGROUND_COLOR = "#141c15"
    DEFAULT_OPTIONS = {"bg": BACKGROUND_COLOR, "highlightbackground": BACKGROUND_COLOR}

    def __init__(self, root: Tk):
        self.__root = root
        self.__root.title("FFMPEG Default Changer")

        self.__file_entry_row = 0
        self.__inspect_file_button_row = 1
        self.__subtitles_dropdown_row = 3
        self.__audio_dropdown_row = 2
        self.__attachment_dropdown_row = 4
        self.__buttons_component_row = 50

        self.__service_message_row = 100

        self.__file_entry_text = None
        self.__default_attachment = None
        self.__default_audio = None
        self.__default_subtitle = None

        self.__service_message = None
        self.__subtitles_list = []
        self.__audio_list = []
        self.__attachments_list = []
        self.__commands = []

    def __create_window(self):
        width = 900
        height = 450
        dimension = f"{width}x{height}"
        self.__root.geometry(dimension)
        self.__root.configure(bg=self.BACKGROUND_COLOR)

    def __build_command(
        self,
        file_path: str,
        audio: str,
        subtitle: str,
        attachment: str,
        output_file_path: str,
    ) -> Iterable[str]:
        builder = FfmpegCommandBuilder(file_path)
        builder.add_stream(audio, StreamType.AUDIO)
        builder.add_stream(subtitle, StreamType.SUBTITLE)
        builder.set_default(audio, StreamType.AUDIO)
        builder.set_default(subtitle, StreamType.SUBTITLE)

        if attachment:
            builder.add_stream(attachment, StreamType.ATTACHMENT)

        command = builder.build(output_file_path)
        self.log_to_console(builder.print_command(), is_clear=False)
        return command

    def __set_default_streams(self):
        path = get_widget_value(self.__file_entry_text)
        audio_number, _, _ = get_widget_value(self.__default_audio).split(":")
        subtitle_number, _, _ = get_widget_value(self.__default_subtitle).split(":")
        # attachment, _ = get_widget_value(self.__default_attachment).split(": ")
        self.log_to_console("")
        files = get_files(path)
        if not files:
            return
        file = files[0]
        out_dir, _ = parse_path(file.path)
        out_path = create_sub_directory(out_dir, "updated")
        self.log_to_console(f"building command for file {file.name}", is_clear=False)
        self.__commands = [
            self.__build_command(
                file_path=file.path,
                audio=audio_number,
                subtitle=subtitle_number,
                attachment=None,
                output_file_path=f"{out_path}/{file.name}",
            )
        ]

    def __find_language_stream(
        self,
        stream_key: str,
        stream_objs: dict[Iterable[MediaStream]],
        find_title,
        find_language,
    ) -> int:
        for index, stream in enumerate(stream_objs.get(stream_key)):
            title = stream.title if stream.title else "None"
            language = stream.language if stream.language else "None"
            if find_title == title and find_language == language:
                return index
        return -1

    def __set_bulk_default_streams(self):
        path = get_widget_value(self.__file_entry_text)
        _, audio_name, audio_language = get_widget_value(self.__default_audio).split(
            ":"
        )
        _, subtitle_name, subtitle_language = get_widget_value(
            self.__default_subtitle
        ).split(":")

        self.log_to_console("")
        files = get_files(path)

        if not files:
            return
        out_dir, _ = parse_path(files[0].path)
        out_path = create_sub_directory(out_dir, "updated")
        commands = []
        for file in files:
            self.log_to_console(
                f"building command for file {file.name}", is_clear=False
            )
            streams = get_media_streams(file.path)
            stream_objs = parse_streams(streams)

            new_audio_number = self.__find_language_stream(
                "audio", stream_objs, audio_name, audio_language
            )
            new_subtitle_number = self.__find_language_stream(
                "subtitle", stream_objs, subtitle_name, subtitle_language
            )
            if new_audio_number == -1 or new_subtitle_number == -1:
                self.log_to_console(
                    f"** could not find the language setting you are looking for {file.name}\n",
                    is_clear=False,
                )
                continue
            command = self.__build_command(
                file_path=file.path,
                audio=new_audio_number,
                subtitle=new_subtitle_number,
                attachment=None,
                output_file_path=f"{out_path}/{file.name}",
            )
            commands.append(command)

        self.__commands = commands

    def __add_audio_component(self):
        create_label(
            self.__root,
            "Audio Streams",
            self.__audio_dropdown_row,
            self.DEFAULT_OPTIONS,
        )
        self.__default_audio, _ = create_dropdown(
            self.__root,
            self.__audio_list,
            self.__audio_dropdown_row,
            lambda x: self.log_to_console(f"selected {x}"),
        )

    def __add_subtitle_component(self):
        create_label(
            self.__root,
            "Subtitle Streams",
            self.__subtitles_dropdown_row,
            self.DEFAULT_OPTIONS,
        )
        self.__default_subtitle, _ = create_dropdown(
            self.__root,
            self.__subtitles_list,
            self.__subtitles_dropdown_row,
            lambda x: self.log_to_console(f"selected {x}"),
        )

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

    def create_options(self, options: Iterable[MediaStream]):
        all_options = [self.BLANK]
        if not options:
            return all_options

        if isinstance(options[0], AudioStream) or isinstance(
            options[0], SubtitleStream
        ):
            language_options = [
                f"{index}:{stream.title}:{stream.language}"
                for index, stream in enumerate(options)
            ]
            all_options.extend(language_options)
        elif isinstance(options[0], AttachmentStream):
            extras_options = [
                f"{index}: {stream.filename}" for index, stream in enumerate(options)
            ]
            all_options.extend(extras_options)
        return all_options

    def __run_commands(self):
        is_okay = create_confirmation_window(
            "Confirmation", "Are you sure you want to run these commands?"
        )

        if not is_okay:
            self.log_to_console("ffmpeg aborted!")
            return

        for command in self.__commands:
            run_shell_command(command)

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
        self.__subtitles_list = self.create_options(stream_objs.get("subtitle"))
        self.__audio_list = self.create_options(stream_objs.get("audio"))
        self.__attachments_list = self.create_options(stream_objs.get("attachment"))
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
