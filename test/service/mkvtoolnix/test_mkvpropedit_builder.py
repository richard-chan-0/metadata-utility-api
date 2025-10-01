from unittest.mock import patch
import pytest
from src.service.mkvtoolnix.mkvpropedit_builder import MkvPropEditCommandBuilder
from src.lib.exceptions.exceptions import FileSystemError
from src.lib.data_types.media_types import StreamType


@pytest.fixture
def builder():
    with patch("src.service.mkvtoolnix.mkvpropedit_builder.is_file", return_value=True):
        builder = MkvPropEditCommandBuilder("test.mkv")
        yield builder


def test_set_track(builder):
    builder.set_track(1, StreamType.AUDIO, True)
    command = builder.build().get_command()
    assert "--edit" in command
    assert "track:a1" in command
    assert "--set" in command
    assert "flag-default=1" in command


def test_set_title(builder):
    builder.set_title("My Custom Title")
    command = builder.build().get_command()
    assert "--edit" in command
    assert "info" in command
    assert "--set" in command
    assert "title=My Custom Title" in command


def test_invalid_file_path():
    with pytest.raises(FileSystemError):
        MkvPropEditCommandBuilder("invalid_path.mkv")


def test_invalid_stream_type(builder):
    with pytest.raises(ValueError):
        builder.set_track(1, "INVALID_TYPE", True)
