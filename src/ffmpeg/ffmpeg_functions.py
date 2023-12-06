from src.utilities.os_functions import run_shell_command, is_dir, get_files
from src.factories.factories import (
    create_audio_stream,
    create_subtitle_stream,
    create_attachment_stream,
)
from typing import Iterable, Callable
from json import loads
from logging import getLogger
from src.data_types.media_types import MediaStream

logger = getLogger(__name__)

media_types = {
    "subtitle": create_subtitle_stream,
    "audio": create_audio_stream,
    "attachment": create_attachment_stream,
}


def get_media_stream_creator(media_type: str) -> Callable:
    if media_type not in media_types:
        logger.info("invalid media type found for %s", media_type)
        return

    return media_types[media_type]


def get_first_file_path(path: str) -> str:
    is_dir_path = is_dir(path)
    if not is_dir_path:
        return path

    files = get_files(path)
    if not files:
        raise FileExistsError("directory is empty")
    return files[0].path


def get_media_streams(path: str) -> Iterable[dict]:
    """function to run ffprobe to get audio, video, subtitle information as json"""
    file_path = get_first_file_path(path)
    shell_output = run_shell_command(
        ["ffprobe", "-hide_banner", "-show_streams", "-print_format", "json", file_path]
    )
    return loads(shell_output.stdout)["streams"]


def parse_streams(streams: Iterable[dict]) -> dict[Iterable[MediaStream]]:
    """function to create object for streams"""
    print(streams)
    media_streams = {}
    for stream_metadata in streams:
        media_type = stream_metadata["codec_type"]
        create_stream = get_media_stream_creator(media_type=media_type)
        if not create_stream:
            continue

        stream_data = create_stream(stream_metadata)
        if media_type not in media_streams:
            media_streams[media_type] = [stream_data]
        else:
            media_streams[media_type].append(stream_data)

    return media_streams
