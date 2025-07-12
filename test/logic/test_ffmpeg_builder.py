from src.logic.ffmpeg_builder import FfmpegCommandBuilder
from src.lib.data_types.media_types import StreamType
from unittest.mock import patch


def test_create_command_happy_path():
    test_path = "test/test.mkv"
    expected = f"ffmpeg -i {test_path} -map 0:v:0 -c copy -map 0:a:1 -map 0:s:1 -disposition:s:0 forced test/updated/test.mkv"

    with patch("src.lib.utilities.os_functions.os") as mock_os:
        mock_os.path.exists.return_value = True
        mock_os.path.split.return_value = ("test", "test.mkv")

        new_builder = FfmpegCommandBuilder(test_path)
        new_builder.add_stream(1, StreamType.AUDIO)
        new_builder.add_stream(1, StreamType.SUBTITLE)
        new_builder.set_default(0, StreamType.SUBTITLE)
        command = new_builder.build()

        assert expected == str(command)
