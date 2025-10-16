from src.lib.exceptions.exceptions import FileSystemError
from src.lib.utilities.os_functions import is_file
from src.lib.data_types.media_types import StreamType
from src.lib.data_types.Command import Command


def get_track_prefix(stream_type):
    if stream_type == StreamType.AUDIO:
        return "a"
    elif stream_type == StreamType.SUBTITLE:
        return "s"
    else:
        raise ValueError("Invalid stream type")


class MkvPropEditCommandBuilder:
    def __init__(self, file_path):
        self.__command = ["mkvpropedit"]
        self.__add_file(file_path)

    def __add_file(self, file_path: str):
        """adds input file for command"""
        if not is_file(file_path):
            raise FileSystemError("invalid file path given")

        self.__command.append(f"{file_path}")

    def set_track(self, stream_number: int, stream_type: StreamType, is_priority: bool):
        stream_letter = get_track_prefix(stream_type)
        default_command = [
            "--edit",
            f"track:{stream_letter}{stream_number}",
            "--set",
            f"flag-default={'1' if is_priority else '0'}",
            "--set",
            "flag-forced=0",
        ]
        self.__command.extend(default_command)

        return self

    def set_title(self, title: str):
        title_command = [
            "--edit",
            "info",
            "--set",
            f"title={title}",
        ]
        self.__command.extend(title_command)

        return self

    def build(self) -> Command:
        return Command(self.__command)
