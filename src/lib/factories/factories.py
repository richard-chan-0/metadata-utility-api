from posix import DirEntry
from src.lib.data_types.DirectoryFile import DirectoryFile
from src.lib.data_types.ServiceArguments import ServiceArguments
from src.lib.data_types.media_types import AudioStream, SubtitleStream, AttachmentStream
from src.lib.utilities.app_functions import read_dict
from re import match


def create_file(dir_entry: DirEntry):
    return DirectoryFile(dir_entry.name, dir_entry.path)


def create_file(name: str, path: str):
    return DirectoryFile(name, path)


def create_basic_service_args(directory_in: str, directory_out: str):
    return ServiceArguments(directory_in, directory_out)


def create_audio_stream(stream: dict):
    language = read_dict("tags.language", stream)
    title = read_dict("tags.title", stream)
    is_default = bool(read_dict("disposition.default", stream))
    stream_number = read_dict("index", stream)
    return AudioStream(
        stream_number=stream_number,
        language=language,
        is_default=is_default,
        title=title,
    )


def create_subtitle_stream(stream: dict):
    language = read_dict("tags.language", stream)
    title = read_dict("tags.title", stream)
    is_default = bool(read_dict("disposition.default", stream))
    stream_number = read_dict("index", stream)
    return SubtitleStream(
        stream_number=stream_number,
        language=language,
        is_default=is_default,
        title=title,
    )


def get_language(track: dict):
    for key in ["Language", "Language (IETF BCP 47)"]:
        if key in track:
            return track[key]

    return "no language"


def create_mkv_subtitle_stream(track: dict, subtitle_number: int):
    language = get_language(track)
    return SubtitleStream(
        stream_number=subtitle_number,
        language=language,
        is_default=track["is_default"] == "1" if "is_default" in track else False,
        title=track["Name"] if "Name" in track else "",
    )


def create_mkv_audio_stream(track: dict, audio_number: int):
    language = get_language(track)
    return AudioStream(
        stream_number=audio_number,
        language=language,
        is_default=track["is_default"] == "1" if "is_default" in track else False,
        title=track["Name"] if "Name" in track else "",
    )


def create_attachment_stream(stream: dict):
    stream_number = read_dict("index", stream)
    file_name = read_dict("tags.filename", stream)
    return AttachmentStream(stream_number, file_name)
