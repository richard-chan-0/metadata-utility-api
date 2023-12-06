from src.exceptions.exceptions import RenameMediaError
from src.data_types.DirectoryFile import DirectoryFile
from re import sub


def prepend_zeros(number: int, number_zeros: int = 3) -> str:
    """function to add zeros until number matches format [0-9]+"""
    str_number = str(number)
    while len(str_number) < number_zeros:
        str_number = f"0{str_number}"

    return f"{str_number}"


def create_calibre_image_name(story: str, chapter: str, page: int) -> str:
    """function to generate name that can be read by calibre"""
    chapter_number = prepend_zeros(chapter)
    page_number = prepend_zeros(page)

    return f"{story} - c{chapter_number} - p{page_number}.png"


def create_jellyfin_episode_name(
    episode_number: int, season_number: int, extension: str
) -> str:
    """function to create an episode name in jellyfin format with episode and season"""
    if season_number < 0 or episode_number < 0:
        raise RenameMediaError("season and episodes can't be negative")

    jellyfin_number_zeros = 2
    season = prepend_zeros(season_number, jellyfin_number_zeros)
    episode = prepend_zeros(episode_number, jellyfin_number_zeros)
    return f"Episode S{season}E{episode}.{extension}"


def create_jellyfin_comic_name(issue: int, story_name: str) -> str:
    jellyfin_number_zeros = 3
    issue_number = prepend_zeros(issue, jellyfin_number_zeros)

    return f"{story_name} #{issue_number}.cbz"


def get_cleanup_regex():
    """function to retrieve regex that cleans up characters in parenthesis or brackets"""
    return "(\(.+\)|\[.+\])"


def cleanup_filename(story_name: str, file: DirectoryFile):
    """function to remove clutter from filename"""
    file_name = file.name
    split_name = file_name.split(".")
    name = split_name[0]
    extensions = ".".join(split_name[1:])
    cleanup_regex = get_cleanup_regex()
    cleaned_name = sub(cleanup_regex, "", name).strip()

    return f"{story_name}-{cleaned_name}.{extensions}"
