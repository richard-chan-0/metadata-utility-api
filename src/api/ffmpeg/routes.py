from flask import Blueprint, request, jsonify
import logging
from src.logic import (
    get_media_streams,
    parse_streams,
    build_command,
    run_shell_command,
    get_mkv_media_streams,
)
from src.lib.utilities.os_functions import get_files
from ast import literal_eval
from os import getenv

logger = logging.getLogger(__name__)

ffmpeg = Blueprint("ffmpeg", __name__, url_prefix="/ffmpeg")


@ffmpeg.route("/write", methods=["POST"])
def write_streams():
    data = request.form
    path = data["path"]
    subtitle_numbers = literal_eval(data["subtitles"])
    audio_numbers = literal_eval(data["audios"])

    files = get_files(path)
    if not files:
        return jsonify(f"no files found for path: {path}")

    for file in files:
        command = build_command(
            file_path=file.path,
            audio=audio_numbers,
            subtitle=subtitle_numbers,
            attachment=None,
        )
        run_shell_command(command)
    return jsonify("successfully reset default audios for files in path")
