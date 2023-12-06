from src.exceptions.exceptions import DataTypeError, FileSystemError
from src.utilities.os_functions import is_file
from src.data_types.media_types import StreamType


class FfmpegCommandBuilder:
    def __init__(self, file_path, video_stream: int = 0):
        self.__command = ["ffmpeg"]
        self.__add_file(file_path)
        self.__add_video(video_stream)

    def __add_file(self, file_path: str):
        """adds input file for command"""
        if not is_file(file_path):
            raise FileSystemError("invalid file path given")

        command = ["-i", f"{file_path}"]
        self.__command.extend(command)

    def __create_stream(self, stream_number: int, stream_type: StreamType):
        if stream_type == StreamType.AUDIO:
            return f"a:{stream_number}"
        elif stream_type == StreamType.SUBTITLE:
            return f"s:{stream_number}"
        elif stream_type == StreamType.ATTACHMENT:
            return f"t:{stream_number}"
        return f"{stream_number}"

    def __add_video(self, stream_number: int = 0):
        """maps the video stream into the command, should be zero"""
        video_command = ["-map", f"0:v:{stream_number}", "-c", "copy"]
        self.__command.extend(video_command)

        return self

    def add_stream(self, stream_number: int, stream_type: StreamType):
        """maps the subtitle stream into the command"""
        stream = self.__create_stream(stream_number, stream_type)
        stream_command = ["-map", f"0:{stream}"]
        self.__command.extend(stream_command)

        return self

    def set_default(self, stream_number: int, stream_type: StreamType):
        stream = self.__create_stream(stream_number, stream_type)
        default_command = [f"-disposition:{stream}", "default"]
        self.__command.extend(default_command)

        return self

    def __set_output_file(self, output_file_path: str):
        output_command = [f"{output_file_path}"]
        self.__command.extend(output_command)
        return self

    def print_command(self):
        return " ".join(self.__command)

    def build(self, output_file_path):
        self.__set_output_file(output_file_path)
        return self.__command
