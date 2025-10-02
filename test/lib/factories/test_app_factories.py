import pytest
from src.lib.factories.app_factories import (
    create_file_by_name,
    create_basic_service_args,
    create_audio_stream,
    create_subtitle_stream,
    create_mkv_audio_stream,
    create_mkv_subtitle_stream,
    create_attachment_stream,
)
from src.lib.data_types.DirectoryFile import DirectoryFile
from src.lib.data_types.ServiceArguments import ServiceArguments
from src.lib.data_types.media_types import AudioStream, SubtitleStream, AttachmentStream
from unittest.mock import MagicMock


def test_create_file_with_name_and_path():
    file = create_file_by_name("test_file.txt", "/path/to/test_file.txt")
    assert isinstance(file, DirectoryFile)
    assert file.name == "test_file.txt"
    assert file.path == "/path/to/test_file.txt"


def test_create_basic_service_args():
    args = create_basic_service_args("/input", "/output")
    assert isinstance(args, ServiceArguments)
    assert args.directory_in == "/input"
    assert args.directory_out == "/output"


def test_create_audio_stream():
    stream_data = {
        "tags": {"language": "en", "title": "English Audio"},
        "disposition": {"default": 1},
        "index": 0,
    }
    audio_stream = create_audio_stream(stream_data)
    assert isinstance(audio_stream, AudioStream)
    assert audio_stream.language == "en"
    assert audio_stream.title == "English Audio"
    assert audio_stream.is_default is True
    assert audio_stream.stream_number == 0


def test_create_subtitle_stream():
    stream_data = {
        "tags": {"language": "fr", "title": "French Subtitles"},
        "disposition": {"default": 0},
        "index": 1,
    }
    subtitle_stream = create_subtitle_stream(stream_data)
    assert isinstance(subtitle_stream, SubtitleStream)
    assert subtitle_stream.language == "fr"
    assert subtitle_stream.title == "French Subtitles"
    assert subtitle_stream.is_default is False
    assert subtitle_stream.stream_number == 1


def test_create_mkv_audio_stream():
    track_data = {"Language": "es", "is_default": "1", "Name": "Spanish Audio"}
    audio_stream = create_mkv_audio_stream(track_data, 2)
    assert isinstance(audio_stream, AudioStream)
    assert audio_stream.language == "es"
    assert audio_stream.title == "Spanish Audio"
    assert audio_stream.is_default is True
    assert audio_stream.stream_number == 2


def test_create_mkv_subtitle_stream():
    track_data = {"Language": "de", "is_default": "0", "Name": "German Subtitles"}
    subtitle_stream = create_mkv_subtitle_stream(track_data, 3)
    assert isinstance(subtitle_stream, SubtitleStream)
    assert subtitle_stream.language == "de"
    assert subtitle_stream.title == "German Subtitles"
    assert subtitle_stream.is_default is False
    assert subtitle_stream.stream_number == 3


def test_create_attachment_stream():
    stream_data = {"index": 4, "tags": {"filename": "attachment.txt"}}
    attachment_stream = create_attachment_stream(stream_data)
    assert isinstance(attachment_stream, AttachmentStream)
    assert attachment_stream.stream_number == 4
    assert attachment_stream.filename == "attachment.txt"
