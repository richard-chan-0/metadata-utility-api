from src.lib.data_types.Command import Command
from src.lib.utilities.os_functions import run_shell_command
from src.lib.factories.app_factories import (
    create_mkv_audio_stream,
    create_mkv_subtitle_stream,
)
from re import findall

mkv_stream_constructors = {
    "audio": create_mkv_audio_stream,
    "subtitles": create_mkv_subtitle_stream,
}

skip_attributes = [
    "Cluster",
    '"Lacing" flag',
    "Edition flag hidden",
    "Edition flag default",
    "Edition UID",
    "Chapter UID",
    "Chapter flag hidden",
    "Chapter flag enabled",
    "Chapter time start",
    "Track UID",
    "Codec ID",
    "Default duration",
    "Written application",
    "Segment UID",
    "EBML version",
    "EBML read version",
    "Maximum EBML ID length",
    "Maximum EBML size length",
    "Document type version",
    "Document type read versjion",
]


def probe_mkv(path):
    probe = Command(["mkvinfo", path])
    return run_shell_command(probe)


def add_attribute(pointer, attributes, attribute):
    attribute_name, attribute_value = attribute.split(":", 1)
    if attribute_name in skip_attributes:
        return pointer + 1

    attribute_name = attribute_name.strip()
    attribute_name = (
        attribute_rename_map[attribute_name]
        if attribute_name in attribute_rename_map
        else attribute_name
    )
    attributes[attribute_name] = attribute_value.strip()
    return pointer + 1


attribute_rename_map = {
    '"Default track" flag': "is_default",
}


def parse_mkv(curr_level, pointer, mkv_data, mkv_parsed):
    _, feature = mkv_data[pointer].split("+", 1)
    feature = feature.strip().split(":", 1)[0]
    attributes = {}
    pointer += 1
    while True:
        if pointer >= len(mkv_data) - 1:
            break

        level_desc, attribute = mkv_data[pointer].split("+", 1)
        attribute = attribute.strip()

        level = len(level_desc)
        if level <= curr_level:
            break

        pointer = (
            parse_mkv(level, pointer, mkv_data, attributes)
            if len(attribute.split(":", 1)) == 1
            else add_attribute(pointer, attributes, attribute)
        )

    if feature not in mkv_parsed:
        mkv_parsed[feature.strip()] = attributes
        return pointer

    if isinstance(mkv_parsed[feature.strip()], list):
        mkv_parsed[feature.strip()].append(attributes)
    else:
        mkv_parsed[feature.strip()] = [mkv_parsed[feature.strip()], attributes]

    return pointer


def get_mkv_payload(mkv):
    pointer = 0
    data = mkv.split("\n")
    mkv_parsed = {}
    while pointer < len(data):
        pointer += parse_mkv(0, pointer, data, mkv_parsed)

    return mkv_parsed


def get_track_number(track_number_str: str) -> tuple[int, int]:
    """
    parses track number in following format and returns list of two integers
    ex. 2 (track ID for mkvmerge & mkvextract: 1)
    """
    matches = findall(r"(\d+)", track_number_str)
    if not matches:
        return (-1, -1)
    return tuple([int(num) for num in matches])


def parse_tracks(mkv):
    mkv_tracks = {"audio": [], "subtitle": []}
    tracks = mkv["Segment"]["Tracks"]["Track"]
    for track in tracks:
        track_type = track["Track type"]
        if track_type not in mkv_stream_constructors:
            continue

        media_type = track_type if track_type != "subtitles" else "subtitle"
        relative_track_number = len(mkv_tracks[media_type]) + 1
        absolute_track_number, merge_track_number = get_track_number(
            track["Track number"]
        )

        stream_function = mkv_stream_constructors[track_type]
        stream = stream_function(
            track, relative_track_number, absolute_track_number, merge_track_number
        )
        mkv_tracks[media_type].append(stream)

    return mkv_tracks


def get_mkv_media_streams(path):
    mkv = probe_mkv(path)
    if not mkv:
        return {}

    mkv_payload = get_mkv_payload(mkv)

    return {"is_mkv": True, **parse_tracks(mkv_payload)}
