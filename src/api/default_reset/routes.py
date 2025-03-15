from flask import Blueprint, request, jsonify
import logging
from src.ffmpeg.ffmpeg_functions import get_media_streams, parse_streams

logger = logging.getLogger(__name__)

default_reset = Blueprint("default_reset", __name__, url_prefix="/default_reset")


@default_reset.route("/")
def default_reset_home():
    return "default reset endpoint"


@default_reset.route("/streams", methods=["POST"])
def read_streams():
    data = request.form
    path = data["path"]
    raw_streams = get_media_streams(path)
    response = parse_streams(raw_streams)
    return jsonify(response)
