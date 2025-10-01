import pytest
from flask import Flask
from flask.testing import FlaskClient
from src.api.mkvtoolnix.routes import mkvtoolnix
from unittest.mock import patch, MagicMock
from src.lib.exceptions.exceptions import ServiceError, RequestError


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(mkvtoolnix)
    app.config["TESTING"] = True

    @app.errorhandler(RequestError)
    def handle_request_error(e):
        return {"error": str(e)}, 400

    @app.errorhandler(ServiceError)
    def handle_service_error(e):
        return {"error": str(e)}, 500

    return app.test_client()


def test_write_streams_success(client: FlaskClient):
    with patch("src.api.mkvtoolnix.routes.getenv", return_value="/mock/path"), patch(
        "src.api.mkvtoolnix.routes.get_files", return_value=True
    ), patch(
        "src.api.mkvtoolnix.routes.create_mkvtoolnix_write_request"
    ) as mock_request, patch(
        "src.api.mkvtoolnix.routes.build_edit_command", return_value="mock_command"
    ), patch(
        "src.api.mkvtoolnix.routes.run_shell_command", return_value="success"
    ) as mock_run:

        mock_request.return_value = MagicMock(
            filename="test.mkv",
            default_audio=[0],
            default_subtitle=[1],
            video_title="Test Title",
        )

        response = client.post("/mkv/write", json={"filename": "test.mkv"})

        assert response.status_code == 200
        assert b"successfully reset default tracks" in response.data
        mock_run.assert_called_once_with("mock_command")


def test_merge_streams_success(client: FlaskClient):
    with patch("src.api.mkvtoolnix.routes.getenv", return_value="/mock/path"), patch(
        "src.api.mkvtoolnix.routes.get_files", return_value=True
    ), patch(
        "src.api.mkvtoolnix.routes.create_mkvtoolnix_merge_request"
    ) as mock_request, patch(
        "src.api.mkvtoolnix.routes.build_merge_command", return_value="mock_command"
    ), patch(
        "src.api.mkvtoolnix.routes.run_shell_command", return_value="success"
    ) as mock_run:

        mock_request.return_value = MagicMock(
            filename="input.mkv",
            output_filename="output.mkv",
            audio_tracks=[0],
            subtitle_tracks=[1],
        )

        response = client.post(
            "/mkv/merge",
            json={"filename": "input.mkv", "output_filename": "output.mkv"},
        )

        assert response.status_code == 200
        assert b"successfully merged input.mkv to output.mkv" in response.data
        mock_run.assert_called_once_with("mock_command")


def test_write_streams_no_env_var(client: FlaskClient):
    with patch("src.api.mkvtoolnix.routes.getenv", return_value=None):
        response = client.post("/mkv/write", json={"filename": "test.mkv"})
        assert response.status_code == 500
        assert response.json == {"error": "environment variable not set"}


def test_merge_streams_no_files(client: FlaskClient):
    with patch("src.api.mkvtoolnix.routes.getenv", return_value="/mock/path"), patch(
        "src.api.mkvtoolnix.routes.get_files", return_value=False
    ):

        response = client.post(
            "/mkv/merge",
            json={"filename": "input.mkv", "output_filename": "output.mkv"},
        )
        assert response.status_code == 500
        assert response.json == {"error": "no files found in path"}
