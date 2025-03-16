from src.utilities.os_functions import run_shell_command, is_dir, get_files
from src.factories.factories import (
    create_audio_stream,
    create_subtitle_stream,
    create_attachment_stream,
)
from typing import Iterable, Callable
from json import loads
from logging import getLogger
from src.data_types.media_types import *
from src.ffmpeg.ffmpeg_builder import FfmpegCommandBuilder
from src.data_types.FfmpegCommand import FfmpegCommand

logger = getLogger(__name__)

# TODO: figure out what attachments are used for
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
    output = loads(shell_output.stdout)
    return output["streams"]


def parse_streams(streams: Iterable[dict]) -> dict[Iterable[MediaStream]]:
    """function to create object for streams"""
    logger.info(streams)
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


def get_matching_stream_numbers(stream_type, all_streams_details, media_streams):
    new_subtitle_numbers = []

    for subtitle_details in all_streams_details:
        _, subtitle_name, subtitle_language = subtitle_details
        new_subtitle_number = find_language_stream(
            stream_type, media_streams, subtitle_name, subtitle_language
        )
        if new_subtitle_number == -1:
            continue
        new_subtitle_numbers.append(new_subtitle_number)
    return new_subtitle_numbers


def find_language_stream(
    stream_key: str,
    media_streams: dict[Iterable[MediaStream]],
    find_title,
    find_language,
) -> int:
    for index, stream in enumerate(media_streams.get(stream_key)):
        title = stream.title if stream.title else "None"
        language = stream.language if stream.language else "None"
        if find_title == title and find_language == language:
            return index
    return -1


def create_options(options: Iterable[MediaStream]):
    all_options = ["n/a"]
    if not options:
        return all_options

    if isinstance(options[0], AudioStream) or isinstance(options[0], SubtitleStream):
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


def build_command(
    file_path: str,
    audios: Iterable[str],
    subtitles: Iterable[str],
    attachment: str,
) -> FfmpegCommand:
    builder = FfmpegCommandBuilder(file_path)
    for audio in set(audios):
        builder.add_stream(audio, StreamType.AUDIO)
    for subtitle in set(subtitles):
        builder.add_stream(subtitle, StreamType.SUBTITLE)
    builder.set_default(audios[0], StreamType.AUDIO)
    builder.set_default(subtitles[0], StreamType.SUBTITLE)

    if attachment:
        builder.add_stream(attachment, StreamType.ATTACHMENT)

    return builder.build()
