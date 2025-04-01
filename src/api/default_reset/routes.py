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

default_reset = Blueprint("default_reset", __name__, url_prefix="/default_reset")


@default_reset.route("/mkv", methods=["GET"])
def default_reset_home():
    path = getenv("MKV_DIRECTORY")
    if not path:
        return jsonify("no path set"), 500
    streams = get_mkv_media_streams(path)
    return jsonify(streams)


@default_reset.route("/read", methods=["GET"])
def read_streams():
    path = getenv("MKV_DIRECTORY")
    if not path:
        return jsonify("no path set"), 500
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
