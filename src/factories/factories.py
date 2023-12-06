from posix import DirEntry
from src.data_types.DirectoryFile import DirectoryFile
from src.data_types.ServiceArguments import ServiceArguments
from src.data_types.media_types import AudioStream, SubtitleStream, AttachmentStream
from src.utilities.app_functions import read_dict


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


def create_attachment_stream(stream: dict):
    stream_number = read_dict("index", stream)
    file_name = read_dict("tags.filename", stream)
    return AttachmentStream(stream_number, file_name)
