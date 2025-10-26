from dataclasses import dataclass
from abc import ABC
from enum import Enum


class StreamType(Enum):
    AUDIO = 1
    SUBTITLE = 2
    ATTACHMENT = 3


class MediaStream(ABC):
    pass


@dataclass
class AudioStream(MediaStream):
    stream_number: int
    title: str
    language: str
    is_default: bool
    is_forced: bool


@dataclass
class MkvAudioStream(AudioStream):
    absolute_track_number: int
    merge_track_number: int


@dataclass
class SubtitleStream(MediaStream):
    stream_number: int
    title: str
    language: str
    is_default: bool
    is_forced: bool


@dataclass
class MkvSubtitleStream(SubtitleStream):
    absolute_track_number: int
    merge_track_number: int


@dataclass
class AttachmentStream(MediaStream):
    stream_number: int
    filename: str
