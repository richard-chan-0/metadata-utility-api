from dataclasses import dataclass


@dataclass
class ServiceArguments:
    directory_in: str
    directory_out: str
    start_number: str = ""
    story: str = "n/a"
    chapter: str = "1"
    organization_file: str = "organize_chapters_to_vol.json"
    season_number: str = "1"
    extension: str = "mkv"
