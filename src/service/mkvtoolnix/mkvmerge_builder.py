from src.lib.exceptions.exceptions import FileSystemError
from src.lib.utilities.os_functions import is_file
from src.lib.data_types.Command import Command


class MkvMergeCommandBuilder:
    def __init__(self, output_file: str):
        self.__command = ["mkvmerge", "-o", output_file]
        self.__input_file = None

    def set_input_file(self, file_path: str):
        """Sets the input file for the command"""
        if not is_file(file_path):
            raise FileSystemError("Invalid file path given")

        self.__input_file = file_path
        return self

    def set_audio_tracks(self, track_ids: list):
        """Sets the audio tracks to include"""
        if track_ids:
            self.__command.extend(["--audio-tracks", ",".join(map(str, track_ids))])
        return self

    def set_subtitle_tracks(self, track_ids: list):
        """Sets the subtitle tracks to include"""
        if track_ids:
            self.__command.extend(["--subtitle-tracks", ",".join(map(str, track_ids))])
        return self

    def set_video_tracks(self, track_ids: list):
        """Sets the video tracks to include"""
        if track_ids:
            self.__command.extend(["--video-tracks", ",".join(map(str, track_ids))])
        return self

    def build(self) -> Command:
        """Builds the final command"""
        if not self.__input_file:
            raise FileSystemError("Input file must be set before building the command")

        self.__command.append(self.__input_file)
        return Command(self.__command)
