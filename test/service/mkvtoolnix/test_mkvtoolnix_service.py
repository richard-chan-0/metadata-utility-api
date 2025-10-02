import pytest
from unittest.mock import patch, MagicMock
from src.service.mkvtoolnix.mkvtoolnix_service import (
    get_mkvinfo,
    build_edit_command,
    build_merge_command,
)
from src.lib.data_types.Command import Command
from src.lib.data_types.media_types import StreamType


def test_build_edit_command():
    with patch(
        "src.service.mkvtoolnix.mkvtoolnix_service.MkvPropEditCommandBuilder"
    ) as MockBuilder:
        mock_builder = MockBuilder.return_value
        mock_builder.build.return_value = Command("mock_command")

        command = build_edit_command(
            file_path="/path/to/file.mkv",
            default_audio=1,
            default_subtitle=2,
            title="Test Title",
        )

        assert isinstance(command, Command)
        assert command.get_command() == "mock_command"

        mock_builder.set_track.assert_any_call(1, StreamType.AUDIO, True)
        mock_builder.set_track.assert_any_call(2, StreamType.SUBTITLE, True)
        mock_builder.set_title.assert_called_once_with("Test Title")
        mock_builder.build.assert_called_once()


def test_build_merge_command():
    with patch(
        "src.service.mkvtoolnix.mkvtoolnix_service.MkvMergeCommandBuilder"
    ) as MockBuilder:
        mock_builder = MockBuilder.return_value
        mock_builder.build.return_value = Command("mock_merge_command")

        command = build_merge_command(
            input_file="/path/to/input.mkv",
            output_file="/path/to/output.mkv",
            audio_tracks=[1, 2],
            subtitle_tracks=[3, 4],
        )

        assert isinstance(command, Command)
        assert command.get_command() == "mock_merge_command"

        mock_builder.set_input_file.assert_called_once_with("/path/to/input.mkv")
        mock_builder.set_audio_tracks.assert_called_once_with([1, 2])
        mock_builder.set_subtitle_tracks.assert_called_once_with([3, 4])
        mock_builder.set_video_tracks.assert_called_once_with([0])
        mock_builder.build.assert_called_once()
