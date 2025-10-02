from ast import literal_eval
from src.lib.data_types.mkvtoolnix import MkvToolNixMergeRequest, MkvToolNixWriteRequest
from logging import getLogger

logger = getLogger(__name__)


def create_mkvtoolnix_write_request(data):
    logger.info("Creating MKVToolNix write request")

    filename = data.get("filename")
    video_title = data.get("video_title")
    default_subtitle = data.get("default_subtitle")
    default_audio = data.get("default_audio")

    return MkvToolNixWriteRequest(
        filename=filename,
        video_title=video_title,
        default_audio=default_audio,
        default_subtitle=default_subtitle,
    )


def create_mkvtoolnix_merge_request(data):
    logger.info("Creating MKVToolNix merge request")
    filename = data.get("filename")
    output_filename = data.get("output_filename")
    subtitles = literal_eval(data.get("subtitle_tracks", "[]"))
    audios = literal_eval(data.get("audio_tracks", "[]"))

    return MkvToolNixMergeRequest(
        filename=filename,
        output_filename=output_filename,
        audio_tracks=audios,
        subtitle_tracks=subtitles,
    )
