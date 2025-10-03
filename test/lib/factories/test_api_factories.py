import pytest
from src.lib.factories.api_factories import (
    create_mkvtoolnix_write_request,
    create_mkvtoolnix_merge_request,
)
from src.lib.data_types.mkvtoolnix import MkvToolNixWriteRequest, MkvToolNixMergeRequest


def test_create_mkvtoolnix_write_request():
    data = {
        "filename": "test.mkv",
        "video_title": "Test Video",
        "default_audio": [1],
        "default_subtitle": [2],
    }

    request = create_mkvtoolnix_write_request(data)

    assert isinstance(request, MkvToolNixWriteRequest)
    assert request.filename == "test.mkv"
    assert request.video_title == "Test Video"
    assert request.default_audio == [1]
    assert request.default_subtitle == [2]


def test_create_mkvtoolnix_merge_request():
    data = {
        "filename": "input.mkv",
        "output_filename": "output.mkv",
        "audio_tracks": "[0, 1]",
        "subtitle_tracks": "[2, 3]",
    }

    request = create_mkvtoolnix_merge_request(data)

    assert isinstance(request, MkvToolNixMergeRequest)
    assert request.filename == "input.mkv"
    assert request.output_filename == "output.mkv"
    assert request.audio_tracks == [0, 1]
    assert request.subtitle_tracks == [2, 3]
