from unittest.mock import patch
import pytest
from src.service.mkvtoolnix.mkvmerge_builder import MkvMergeCommandBuilder
from src.lib.exceptions.exceptions import FileSystemError


@pytest.fixture
def builder():
    with patch("src.service.mkvtoolnix.mkvmerge_builder.is_file", return_value=True):
        builder = MkvMergeCommandBuilder("output.mkv")
        builder.set_input_file("input.mkv")
        yield builder


def test_set_input_file(builder):
    command = builder.build().get_command()
    assert "input.mkv" in command


def test_set_audio_tracks(builder):
    builder.set_audio_tracks([1, 2])
    command = builder.build().get_command()
    assert "--audio-tracks" in command
    assert "1,2" in command


def test_set_subtitle_tracks(builder):
    builder.set_subtitle_tracks([3, 4])
    command = builder.build().get_command()
    assert "--subtitle-tracks" in command
    assert "3,4" in command


def test_set_video_tracks(builder):
    builder.set_video_tracks([0])
    command = builder.build().get_command()
    assert "--video-tracks" in command
    assert "0" in command


def test_missing_input_file():
    builder = MkvMergeCommandBuilder("output.mkv")
    with pytest.raises(FileSystemError):
        builder.build()
