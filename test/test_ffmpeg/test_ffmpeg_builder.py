from src.ffmpeg.ffmpeg_builder import FfmpegCommandBuilder
from src.data_types.media_types import StreamType
from unittest.mock import patch


def test_create_command_happy_path():
    test_path = "test.mkv"
    expected = f"ffmpeg -i {test_path} -map 0 -c copy -map -0:a:1 -map -0:s:1 -disposition:s:0 default -n {test_path}"

    with patch("src.utilities.os_functions.os") as mock_os:
        mock_os.path.exists.return_value = True

        new_builder = FfmpegCommandBuilder(test_path)
        new_builder.add_stream(1, StreamType.AUDIO)
        new_builder.add_stream(1, StreamType.SUBTITLE)
        new_builder.set_default(0, StreamType.SUBTITLE)
        new_builder.build()

        assert expected == new_builder.print_command()
