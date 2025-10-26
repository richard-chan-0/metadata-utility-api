from posix import DirEntry
from src.lib.data_types.DirectoryFile import DirectoryFile
from src.lib.data_types.ServiceArguments import ServiceArguments
from src.lib.data_types.media_types import (
    AudioStream,
    SubtitleStream,
    AttachmentStream,
    MkvSubtitleStream,
    MkvAudioStream,
)
from src.lib.utilities.app_functions import read_dict


def create_file_by_name(name: str, path: str):
    return DirectoryFile(name, path)


def create_basic_service_args(directory_in: str, directory_out: str):
    return ServiceArguments(directory_in, directory_out)


def create_audio_stream(stream: dict):
    language = read_dict("tags.language", stream)
    title = read_dict("tags.title", stream)
    is_default = bool(read_dict("disposition.default", stream))
    is_forced = False
    stream_number = read_dict("index", stream)
    return AudioStream(
        stream_number=stream_number,
        language=language,
        is_default=is_default,
        title=title,
        is_forced=is_forced,
    )


def create_subtitle_stream(stream: dict):
    language = read_dict("tags.language", stream)
    title = read_dict("tags.title", stream)
    is_default = bool(read_dict("disposition.default", stream))
    is_forced = False
    stream_number = read_dict("index", stream)
    return SubtitleStream(
        stream_number=stream_number,
        language=language,
        is_default=is_default,
        title=title,
        is_forced=is_forced,
    )


def get_language(track: dict):
    for key in ["Language", "Language (IETF BCP 47)"]:
        if key in track:
            return track[key]

    return "no language"


def get_is_attribute_enabled(attribute: str, track: dict):
    if attribute in track:
        return track[attribute] == "1"
    return False


def get_is_default(track: dict):
    keys = ['"Default track" flag', "is_default"]
    for key in keys:
        if get_is_attribute_enabled(key, track):
            return True
    return False


def get_is_forced(track: dict):
    keys = ['"Forced track" flag', "is_forced"]
    for key in keys:
        if get_is_attribute_enabled(key, track):
            return True
    return False


def create_mkv_subtitle_stream(
    track: dict,
    subtitle_number: int,
    absolute_track_number: int,
    merge_track_number: int,
):
    language = get_language(track)
    return MkvSubtitleStream(
        stream_number=subtitle_number,
        language=language,
        is_default=get_is_default(track),
        is_forced=get_is_forced(track),
        title=track["Name"] if "Name" in track else "",
        absolute_track_number=absolute_track_number,
        merge_track_number=merge_track_number,
    )


def create_mkv_audio_stream(
    track: dict, audio_number: int, absolute_track_number: int, merge_track_number: int
):
    language = get_language(track)
    return MkvAudioStream(
        stream_number=audio_number,
        language=language,
        is_default=get_is_default(track),
        is_forced=get_is_forced(track),
        title=track["Name"] if "Name" in track else "",
        absolute_track_number=absolute_track_number,
        merge_track_number=merge_track_number,
    )


def create_attachment_stream(stream: dict):
    stream_number = read_dict("index", stream)
    file_name = read_dict("tags.filename", stream)
    return AttachmentStream(stream_number, file_name)
