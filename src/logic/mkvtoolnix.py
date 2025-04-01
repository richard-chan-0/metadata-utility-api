from src.lib.data_types.Command import Command
from src.lib.utilities.os_functions import run_shell_command, get_first_file_path
from json import loads

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
    file_path = get_first_file_path(path)
    probe = Command(["mkvinfo", file_path])
    return run_shell_command(probe)


def add_attribute(pointer, attributes, attribute):
    attribute_name, attribute_value = attribute.split(":", 1)
    if attribute_name in skip_attributes:
        return pointer + 1
    attributes[attribute_name.strip()] = attribute_value.strip()
    return pointer + 1


def parse_mkv(curr_level, pointer, mkv_data, mkv_parsed):
    _, feature = mkv_data[pointer].split("+", 1)
    feature = feature.strip()
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


def get_mkv_media_streams(path):
    mkv = probe_mkv(path)
    if not mkv:
        return {}

    mkv_payload = get_mkv_payload(mkv)

    # TODO: get streams

    return mkv_payload
