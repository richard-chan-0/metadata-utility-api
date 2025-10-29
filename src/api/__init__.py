from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from src.api.ffmpeg.routes import ffmpeg
from src.api.mkvtoolnix.routes import mkvtoolnix
from src.lib.exceptions.exceptions import ServiceError, RequestError
from os import getenv
from src.service.mkvtoolnix.mkvtoolnix_service import get_mkv_media_streams
from src.service.ffmpeg import get_media_streams, parse_streams
from src.lib.utilities.os_functions import get_files, is_mkv
from src.lib.utilities.path_validator import validate_query_path

logger = logging.getLogger(__name__)


def register_errors(app):

    @app.errorhandler(RequestError)
    def handle_request_error(e):
        return jsonify({"error": str(e)}), 400

    @app.errorhandler(ServiceError)
    def handle_service_error(e):
        return jsonify({"error": str(e)}), 500

    @app.errorhandler(500)
    def handle_internal_server_error(e):
        return jsonify({"error": str(e)}), 500

    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        return jsonify({"error": str(e)}), 405


def create_app():
    app = Flask("metadata utility")

    app.register_blueprint(ffmpeg)
    app.register_blueprint(mkvtoolnix)

    register_errors(app)

    CORS(app)

    @app.route("/", methods=["GET"])
    def home():
        return "ffmpeg api is running"

    @app.route("/read", methods=["GET"])
    def read_streams():
        query = request.args.get("path")
        validate_query_path(query)
        path = query if query else getenv("MKV_DIRECTORY")
        if not path:
            raise ServiceError("environment variable not set")
        file_paths = get_files(path)
        streams = {}
        for file_path in file_paths:
            if is_mkv(file_path.path):
                streams[file_path.name] = get_mkv_media_streams(file_path.path)
            else:
                raw_streams = get_media_streams(file_path.path)
                streams[file_path.name] = parse_streams(raw_streams)

        return streams

    return app
