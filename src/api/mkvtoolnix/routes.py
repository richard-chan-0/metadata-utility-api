from flask import Blueprint, request, jsonify
import logging
from src.logic.mkvtoolnix import (
    build_command,
    run_shell_command,
)
from src.lib.utilities.os_functions import get_files
from os import getenv
from ast import literal_eval

logger = logging.getLogger(__name__)

mkvtoolnix = Blueprint("mkv", __name__, url_prefix="/mkv")


@mkvtoolnix.route("/write", methods=["POST"])
def write_streams():
    data = request.form
    subtitles = literal_eval(data.get("subtitles", []))
    default_subtitle = int(subtitles[0]) if subtitles else None
    audios = literal_eval(data.get("audios", []))
    default_audio = int(audios[0]) if audios else None
    path = getenv("MKV_DIRECTORY")
    if not path:
        return jsonify("no path set"), 500

    files = get_files(path)
    if not files:
        return jsonify(f"no files found for path: {path}"), 500

    for file in files:
        command = build_command(
            file_path=file.path,
            audio=default_audio,
            subtitle=default_subtitle,
        )
        shell_message = run_shell_command(command)
        logger.info(shell_message)

    return jsonify("successfully reset default tracks for files in path")
