import pytest
from src.service.mkvtoolnix.mkvpropedit_builder import MkvPropEditCommandBuilder
from src.lib.exceptions.exceptions import FileSystemError
from src.lib.data_types.media_types import StreamType


def test_set_track():
    builder = MkvPropEditCommandBuilder("test.mkv")
    builder.set_track(1, StreamType.AUDIO, True)
    command = builder.build().to_list()
    assert "--edit" in command
    assert "track:a1" in command
    assert "--set" in command
    assert "flag-default=1" in command


def test_set_title():
    builder = MkvPropEditCommandBuilder("test.mkv")
    builder.set_title("My Custom Title")
    command = builder.build().to_list()
    assert "--edit" in command
    assert "info" in command
    assert "--set" in command
    assert "title=My Custom Title" in command


def test_invalid_file_path():
    with pytest.raises(FileSystemError):
        MkvPropEditCommandBuilder("invalid_path.mkv")


def test_invalid_stream_type():
    builder = MkvPropEditCommandBuilder("test.mkv")
    with pytest.raises(ValueError):
        builder.set_track(1, "INVALID_TYPE", True)
