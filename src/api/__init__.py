from flask import Flask, jsonify
from flask_cors import CORS
import logging
from src.api.ffmpeg.routes import ffmpeg
from src.api.mkvtoolnix.routes import mkvtoolnix
from src.lib.exceptions.exceptions import ServiceError, RequestError
from os import getenv
from src.logic.mkvtoolnix import get_mkv_media_streams
from src.logic.ffmpeg import get_media_streams, parse_streams
from src.lib.utilities.os_functions import get_first_file_path, is_mkv

logger = logging.getLogger(__name__)


def register_errors(app):

    @app.errorhandler(RequestError)
    def handle_request_error(e):
        return jsonify({"error with request": str(e)}), 400

    @app.errorhandler(ServiceError)
    def handle_service_error(e):
        return jsonify({"error in app": str(e)}), 500

    @app.errorhandler(500)
    def handle_internal_server_error(e):
        return jsonify({"error": str(e)}), 500

    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        return jsonify({"error": str(e)}), 405


def create_app():
    app = Flask("ffmpeg utility")

    app.register_blueprint(ffmpeg)
    app.register_blueprint(mkvtoolnix)

    register_errors(app)

    CORS(app)

    @app.route("/read", methods=["GET"])
    def read_streams():
        path = getenv("MKV_DIRECTORY")
        if not path:
            return jsonify("no path set"), 500
        file_path = get_first_file_path(path)
        if is_mkv(file_path):
            response = get_mkv_media_streams(file_path)
        else:
            raw_streams = get_media_streams(file_path)
            response = parse_streams(raw_streams)

        return jsonify(response)

    return app
