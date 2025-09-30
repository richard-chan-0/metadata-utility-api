from ast import literal_eval
from src.lib.data_types.mkvtoolnix import MkvToolNixMergeRequest, MkvToolNixWriteRequest
from logging import getLogger

logger = getLogger(__name__)


def create_mkvtoolnix_write_request(data):
    logger.info("Creating MKVToolNix write request")
    filename = data.get("filename")
    video_title = data.get("title")
    default_subtitle = data.get("subtitle")
    default_audio = data.get("audio")

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
    subtitles = literal_eval(data.get("subtitles", []))
    audios = literal_eval(data.get("audios", []))

    return MkvToolNixMergeRequest(
        filename=filename,
        output_filename=output_filename,
        audio_tracks=audios,
        subtitle_tracks=subtitles,
    )
