from flask import Flask, jsonify
from flask_cors import CORS
import logging
from src.api.default_reset.routes import default_reset
from src.lib.exceptions.exceptions import ServiceError

logger = logging.getLogger(__name__)


def register_errors(app):

    @app.errorhandler(ServiceError)
    def handle_service_error(e):
        return jsonify({"error": str(e)}), 400

    @app.errorhandler(500)
    def handle_internal_server_error(e):
        return jsonify({"error": str(e)}), 500

    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        return jsonify({"error": str(e)}), 405


def create_app():
    app = Flask("ffmpeg utility")

    app.register_blueprint(default_reset)

    register_errors(app)

    CORS(app)
    return app
