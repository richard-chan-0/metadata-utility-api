from flask import Blueprint, request, jsonify
import logging
from src.service.mkvtoolnix.mkvtoolnix_service import (
    build_edit_command,
    build_merge_command,
)
from src.lib.factories.api_factories import (
    create_mkvtoolnix_write_request,
    create_mkvtoolnix_merge_request,
)
from src.lib.utilities.os_functions import get_files, run_shell_command
from os import getenv
from src.lib.exceptions.exceptions import RequestError, ServiceError

logger = logging.getLogger(__name__)

mkvtoolnix = Blueprint("mkv", __name__, url_prefix="/mkv")

# TODO: make write and merge endpoint able to accept bulk filename request


@mkvtoolnix.route("/write", methods=["POST"])
def write_streams():
    path = getenv("MKV_DIRECTORY")
    if not path:
        logger.error("no mkv directory set")
        raise ServiceError("environment variable not set")

    data = request.json
    write_request = create_mkvtoolnix_write_request(data)

    file_path = f"{path}/{write_request.filename}"
    file = get_files(file_path)
    if not file:
        logger.error("no files in path")
        return ServiceError("no files found in path")

    command = build_edit_command(
        file_path=file_path,
        default_audio=write_request.default_audio,
        default_subtitle=write_request.default_subtitle,
        title=write_request.video_title,
    )
    shell_message = run_shell_command(command)
    logger.info(shell_message)

    return jsonify("successfully reset default tracks for files in path")


@mkvtoolnix.route("/merge", methods=["POST"])
def merge_streams():
    path = getenv("MKV_DIRECTORY")
    if not path:
        logger.error("no mkv directory set")
        raise ServiceError("environment variable not set")

    data = request.json
    merge_request = create_mkvtoolnix_merge_request(data)
    input_filename = merge_request.filename
    output_filename = merge_request.output_filename

    if not output_filename or not input_filename:
        raise RequestError("missing required fields")

    input_file_path = f"{path}/{input_filename}"
    output_file_path = f"{path}/{output_filename}"

    input_file = get_files(input_file_path)
    if not input_file:
        logger.error("no files in path")
        raise ServiceError("no files found in path")

    command = build_merge_command(
        input_file=input_file_path,
        output_file=output_file_path,
        audio_tracks=merge_request.audio_tracks,
        subtitle_tracks=merge_request.subtitle_tracks,
    )
    shell_message = run_shell_command(command)
    logger.info(shell_message)

    return jsonify(f"successfully merged {input_filename} to {output_filename}")
