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
        "src.api.mkvtoolnix.routes.build_edit_command"
    ) as mock_command, patch(
        "src.api.mkvtoolnix.routes.run_shell_command", return_value="success"
    ) as mock_run:

        mock_request.side_effect = lambda data: MagicMock(
            filename=data["filename"],
            default_audio=data.get("default_audio", []),
            default_subtitle=data.get("default_subtitle", []),
            video_title=data.get("video_title", ""),
        )

        mock_command.side_effect = (
            lambda file_path, default_audio, default_subtitle, title: MagicMock(
                get_command=lambda: f"edit command for {file_path}"
            )
        )

        response = client.post(
            "/mkv/write",
            json={
                "file1.mkv": {
                    "default_audio": [0],
                    "default_subtitle": [1],
                    "video_title": "Title 1",
                },
                "file2.mkv": {
                    "default_audio": [2],
                    "default_subtitle": [3],
                    "video_title": "Title 2",
                },
            },
        )

        assert response.status_code == 200
        assert b"successfully reset default tracks" in response.data
        assert mock_run.call_count == 2  # Commands are logged, not executed


def test_merge_streams_success(client: FlaskClient):
    with patch("src.api.mkvtoolnix.routes.getenv", return_value="/mock/path"), patch(
        "src.api.mkvtoolnix.routes.get_files", return_value=True
    ), patch(
        "src.api.mkvtoolnix.routes.create_mkvtoolnix_merge_request"
    ) as mock_request, patch(
        "src.api.mkvtoolnix.routes.build_merge_command"
    ) as mock_command, patch(
        "src.api.mkvtoolnix.routes.run_shell_command", return_value="success"
    ) as mock_run:

        mock_request.side_effect = lambda data: MagicMock(
            filename=data["filename"],
            output_filename=data["output_filename"],
            audio_tracks=data.get("audio_tracks", []),
            subtitle_tracks=data.get("subtitle_tracks", []),
        )

        mock_command.side_effect = (
            lambda input_file, output_file, audio_tracks, subtitle_tracks: MagicMock(
                get_command=lambda: f"merge command for {input_file} to {output_file}"
            )
        )

        response = client.post(
            "/mkv/merge",
            json={
                "changes": [
                    {
                        "filename": "file1.mkv",
                        "output_filename": "output1.mkv",
                        "audio_tracks": "[0]",
                        "subtitle_tracks": "[1]",
                    },
                    {
                        "filename": "file2.mkv",
                        "output_filename": "output2.mkv",
                        "audio_tracks": "[2]",
                        "subtitle_tracks": "[3]",
                    },
                ]
            },
        )

        assert response.status_code == 200
        assert b"successfully merged all files" in response.data
        assert mock_run.call_count == 2  # Commands are logged, not executed


def test_write_streams_no_env_var(client: FlaskClient):
    with patch("src.api.mkvtoolnix.routes.getenv", return_value=None):
        response = client.post("/mkv/write", json={"filename": "test.mkv"})
        assert response.status_code == 500
        assert response.json == {"error": "environment variable not set"}


def test_merge_streams_no_files(client: FlaskClient):
    with (
        patch("src.api.mkvtoolnix.routes.getenv", return_value="/mock/path"),
        patch("src.api.mkvtoolnix.routes.get_files", return_value=False),
    ):

        response = client.post(
            "/mkv/merge",
            json={
                "changes": [
                    {
                        "filename": "file1.mkv",
                        "output_filename": "output1.mkv",
                        "audio_tracks": "[0]",
                        "subtitle_tracks": "[1]",
                    },
                    {
                        "filename": "file2.mkv",
                        "output_filename": "output2.mkv",
                        "audio_tracks": "[2]",
                        "subtitle_tracks": "[3]",
                    },
                ]
            },
        )
        assert response.status_code == 500
        assert response.json == {"error": "no files found in path"}
