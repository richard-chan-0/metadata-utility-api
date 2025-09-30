from dataclasses import dataclass


@dataclass
class MkvToolNixWriteRequest:
    filename: str
    video_title: str
    default_audio: int
    default_subtitle: int


@dataclass
class MkvToolNixMergeRequest:
    filename: str
    output_filename: str
    audio_tracks: list[int]
    subtitle_tracks: list[int]
