from src.lib.data_types.Command import Command
from src.service.mkvtoolnix.mkvpropedit_builder import MkvPropEditCommandBuilder
from src.service.mkvtoolnix.mkvmerge_builder import MkvMergeCommandBuilder
from src.service.mkvtoolnix.mkvinfo_processor import get_mkv_media_streams
from src.lib.data_types.media_types import StreamType
from logging import getLogger

logger = getLogger(__name__)


def get_mkvinfo(path: str) -> dict:
    """
    Function to get mkv info from a file path and return as a dictionary
    """
    return get_mkv_media_streams(path)


def build_edit_command(
    file_path: str,
    default_audio: int,
    default_subtitle: int,
    title: str = None,
) -> Command:
    builder = MkvPropEditCommandBuilder(file_path)
    if default_audio:
        builder.set_track(default_audio, StreamType.AUDIO, True)
    if default_subtitle:
        builder.set_track(default_subtitle, StreamType.SUBTITLE, True)
    if title:
        builder.set_title(title)

    return builder.build()


def build_merge_command(
    input_file: str,
    output_file: str,
    audio_tracks: list = None,
    subtitle_tracks: list = None,
) -> Command:
    builder = MkvMergeCommandBuilder(output_file)
    builder.set_input_file(input_file)
    if audio_tracks:
        builder.set_audio_tracks(audio_tracks)
    if subtitle_tracks:
        builder.set_subtitle_tracks(subtitle_tracks)

    builder.set_video_tracks([0])

    return builder.build()
