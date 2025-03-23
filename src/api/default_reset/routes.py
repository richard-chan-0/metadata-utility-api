from flask import Blueprint, request, jsonify
import logging
from src.ffmpeg.ffmpeg_functions import (
    get_media_streams,
    parse_streams,
    get_files,
    build_command,
    run_shell_command,
)
from ast import literal_eval

logger = logging.getLogger(__name__)

default_reset = Blueprint("default_reset", __name__, url_prefix="/default_reset")


@default_reset.route("/")
def default_reset_home():
    return "default reset endpoint"


@default_reset.route("/read", methods=["POST"])
def read_streams():
    data = request.form
    path = data["path"]
    raw_streams = get_media_streams(path)
    response = parse_streams(raw_streams)
    return jsonify(response)


@default_reset.route("/bulk", methods=["POST"])
def write_bulk_streams():
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
            audios=audio_numbers,
            subtitles=subtitle_numbers,
            attachment=None,
        )
        run_shell_command(command)
    return jsonify("successfully reset default audios for files in path")
