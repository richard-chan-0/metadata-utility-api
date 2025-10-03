import pytest
from unittest.mock import patch, MagicMock
from src.service.mkvtoolnix.mkvinfo_processor import (
    get_track_number,
    parse_tracks,
    get_mkv_payload,
    get_mkv_media_streams,
)

# example mkvinfo
data = [
    "+ EBML head",
    "|+ EBML version: 1",
    "|+ EBML read version: 1",
    "|+ Maximum EBML ID length: 4",
    "|+ Maximum EBML size length: 8",
    "|+ Document type: matroska",
    "|+ Document type version: 4",
    "|+ Document type read version: 2",
    "+ Segment: size 1017807292",
    "|+ Seek head (subentries will be skipped)",
    "|+ Segment information",
    "| + Timestamp scale: 1000000",
    "| + Multiplexing application: libebml v1.4.5 + libmatroska v1.7.1",
    "| + Writing application: mkvmerge v90.0 ('Hanging On') 64-bit",
    "| + Duration: 00:24:14.997000000",
    "| + Segment UID: 0x5a 0x08 0x97 0xa3 0xac 0x44 0x7a 0x76 0xe1 0xc2 0xfa 0x35 0x83 0xd2 0xb5 0x88",
    "| + Title: The Cherry Blossom Ring",
    "|+ Tracks",
    "| + Track",
    "|  + Track number: 1 (track ID for mkvmerge & mkvextract: 0)",
    "|  + Track UID: 17215699583972095819",
    "|  + Track type: video",
    '|  + "Lacing" flag: 0',
    "|  + Language: und",
    "|  + Codec ID: V_MPEG4/ISO/AVC",
    "|  + Codec's private data: size 62 (H.264 profile: High @L4.0)",
    "|  + Default duration: 00:00:00.041708333 (23.976 frames/fields per second for a video track)",
    "|  + Language (IETF BCP 47): und",
    "|  + Video track",
    "|   + Pixel width: 1920",
    "|   + Pixel height: 1080",
    "|   + Display width: 1920",
    "|   + Display height: 1080",
    "| + Track",
    "|  + Track number: 2 (track ID for mkvmerge & mkvextract: 1)",
    "|  + Track UID: 3665082638902786894",
    "|  + Track type: audio",
    "|  + Language: jpn",
    "|  + Codec ID: A_AAC",
    "|  + Codec's private data: size 2",
    "|  + Default duration: 00:00:00.021333333 (46.875 frames/fields per second for a video track)",
    "|  + Language (IETF BCP 47): ja",
    "|  + Audio track",
    "|   + Sampling frequency: 48000",
    "|   + Channels: 2",
    '|  + "Default track" flag: 1',
    "| + Track",
    "|  + Track number: 3 (track ID for mkvmerge & mkvextract: 2)",
    "|  + Track UID: 5297701375855271653",
    "|  + Track type: audio",
    '|  + "Default track" flag: 0',
    "|  + Codec ID: A_AAC",
    "|  + Codec's private data: size 2",
    "|  + Default duration: 00:00:00.021333333 (46.875 frames/fields per second for a video track)",
    "|  + Language (IETF BCP 47): en",
    "|  + Audio track",
    "|   + Sampling frequency: 48000",
    "|   + Channels: 2",
    "| + Track",
    "|  + Track number: 4 (track ID for mkvmerge & mkvextract: 3)",
    "|  + Track UID: 13429901884780835169",
    "|  + Track type: subtitles",
    '|  + "Default track" flag: 0',
    '|  + "Forced display" flag: 1',
    '|  + "Lacing" flag: 0',
    "|  + Codec ID: S_TEXT/UTF8",
    "|  + Language (IETF BCP 47): en",
    "|  + Name: Forced",
    '|  + "Hearing impaired" flag: 0',
    '|  + "Original language" flag: 0',
    "| + Track",
    "|  + Track number: 5 (track ID for mkvmerge & mkvextract: 4)",
    "|  + Track UID: 12337307053565360137",
    "|  + Track type: subtitles",
    '|  + "Lacing" flag: 0',
    "|  + Codec ID: S_TEXT/UTF8",
    "|  + Language (IETF BCP 47): en",
    '|  + "Hearing impaired" flag: 0',
    '|  + "Original language" flag: 0',
    '|  + "Default track" flag: 1',
    "|+ EBML void: size 5560",
    "|+ Chapters",
    "| + Edition entry",
    "|  + Edition flag hidden: 0",
    "|  + Edition flag default: 0",
    "|  + Edition flag ordered: 0",
    "|  + Edition UID: 4211572361470553242",
    "|  + Chapter atom",
    "|   + Chapter UID: 3560472682762046931",
    "|   + Chapter time start: 00:00:00.000000000",
    "|   + Chapter flag hidden: 0",
    "|   + Chapter flag enabled: 1",
    "|   + Chapter display",
    "|    + Chapter string: Scene 1",
    "|    + Chapter language: eng",
    "|    + Chapter language (IETF BCP 47): en",
    "|  + Chapter atom",
    "|   + Chapter UID: 13142092591542964397",
    "|   + Chapter time start: 00:08:44.982000000",
    "|   + Chapter flag hidden: 0",
    "|   + Chapter flag enabled: 1",
    "|   + Chapter display",
    "|    + Chapter string: Scene 2",
    "|    + Chapter language: eng",
    "|    + Chapter language (IETF BCP 47): en",
    "|+ EBML void: size 101",
    "|+ Cluster",
]


def test_get_track_number():
    track_number = get_track_number("2 (track ID for mkvmerge & mkvextract: 1)")
    assert track_number == (2, 1)

    track_number = get_track_number("invalid format")
    assert track_number == (-1, -1)


def test_get_mkv_payload():
    payload = get_mkv_payload("\n".join(data))

    assert "Segment" in payload
    assert "Tracks" in payload["Segment"]
    assert "Track" in payload["Segment"]["Tracks"]

    tracks = payload["Segment"]["Tracks"]["Track"]

    assert len(tracks) == 5


def test_parse_tracks():
    mkv_payload = {
        "Segment": {
            "Tracks": {
                "Track": [
                    {
                        "Track type": "audio",
                        "Track number": "2 (track ID for mkvmerge & mkvextract: 1)",
                        "Language": "jpn",
                        "is_default": "1",
                    },
                    {
                        "Track type": "subtitles",
                        "Track number": "4 (track ID for mkvmerge & mkvextract: 3)",
                        "Language": "en",
                        "Name": "Forced",
                        "is_default": "0",
                    },
                ]
            }
        }
    }

    with (
        patch(
            "src.service.mkvtoolnix.mkvinfo_processor.create_mkv_audio_stream"
        ) as mock_audio_stream,
        patch(
            "src.service.mkvtoolnix.mkvinfo_processor.create_mkv_subtitle_stream"
        ) as mock_subtitle_stream,
    ):
        mock_audio_stream.return_value = "mock_audio_stream"
        mock_subtitle_stream.return_value = "mock_subtitle_stream"

        tracks = parse_tracks(mkv_payload)

        assert "audio" in tracks
        assert "subtitle" in tracks
        assert len(tracks["audio"]) == 1
        assert len(tracks["subtitle"]) == 1


def test_get_mkv_media_streams():
    with (
        patch("src.service.mkvtoolnix.mkvinfo_processor.probe_mkv") as mock_probe,
        patch(
            "src.service.mkvtoolnix.mkvinfo_processor.get_mkv_payload"
        ) as mock_payload,
        patch(
            "src.service.mkvtoolnix.mkvinfo_processor.parse_tracks"
        ) as mock_parse_tracks,
    ):
        mock_probe.return_value = "mocked_mkv_data"
        mock_payload.return_value = {"mocked": "payload"}
        mock_parse_tracks.return_value = {"audio": [], "subtitle": []}

        result = get_mkv_media_streams("/path/to/file.mkv")

        assert result == {"is_mkv": True, "audio": [], "subtitle": []}
        mock_probe.assert_called_once_with("/path/to/file.mkv")
        mock_payload.assert_called_once_with("mocked_mkv_data")
        mock_parse_tracks.assert_called_once_with({"mocked": "payload"})
