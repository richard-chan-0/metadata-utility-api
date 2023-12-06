from src.exceptions.exceptions import OrganizeChaptersToVolError
from src.utilities.os_functions import *
from src.data_types.DirectoryFile import DirectoryFile
from src.data_types.ServiceArguments import ServiceArguments
from json import load
from typing import Iterable, Tuple


VOLUMES = "volumes"
VOLUME = "volume"
START_CHAPTER = "startChapter"
END_CHAPTER = "endChapter"


def get_chapters_to_vols_data():
    file_name = get_organization_file()
    file = open(file_name)
    return load(file)


def is_valid_chapter(chapter):
    """function to determine if chapter contains all attributes"""
    is_with_volume = VOLUME in chapter
    is_with_start = START_CHAPTER in chapter
    is_with_end = END_CHAPTER in chapter
    return all([is_with_end, is_with_start, is_with_volume])


def create_mapping_chapters_to_vols() -> dict[str, Tuple[str, str]]:
    """returns content of json organization file"""
    schema = get_chapters_to_vols_data()
    if "volumes" not in schema:
        raise OrganizeChaptersToVolError("expected volumes attribute in schema")

    chapters = schema[VOLUMES]
    mapping = {}
    for chapter in chapters:
        if not is_valid_chapter(chapter):
            raise OrganizeChaptersToVolError("volume missing attribute")

        volume = chapter[VOLUME]
        start_chapter = chapter[START_CHAPTER]
        end_chapter = chapter[END_CHAPTER]
        mapping[volume] = (start_chapter, end_chapter)

    return mapping


def update_chapter_list(
    volume_path: str,
    moved_files: Iterable[DirectoryFile],
    chapters: Iterable[DirectoryFile],
):
    """function to remove chapters that have been moved"""
    volume_files = {"volume_path": volume_path, "chapters": []}
    for file in moved_files:
        volume_files["chapters"].append(file.name)
        chapters.remove(file)

    return volume_files


def move_chapters_for_volume_dir(
    volume_path: str,
    chapter_details: Tuple[str, str],
    chapters: Iterable[DirectoryFile],
):
    """function to move chapter files into a designated volume directory"""
    start_chapter, end_chapter = chapter_details
    moved_files = []

    for chapter in chapters:
        chapter_name = chapter.name
        chapter_path = chapter.path
        chapter_number = chapter.get_chapter_number_from_file()
        if not (start_chapter <= chapter_number <= end_chapter):
            continue

        new_path = create_new_file_path(volume_path, chapter_name)
        move_file(old_path=chapter_path, new_path=new_path)
        moved_files.append(chapter)

    return update_chapter_list(volume_path, moved_files, chapters)


def move_chapters_to_volumes(
    directory_out: str,
    chapters: Iterable[DirectoryFile],
    mapping: dict[str, Tuple[str, str]],
):
    """creates directories for volumes and moves files into those directories"""
    for volume, chapter_details in mapping.items():
        sub_directory = create_sub_directory(directory_out, volume)
        move_chapters_for_volume_dir(sub_directory, chapter_details, chapters)


def organize_chapters_to_vol(args: ServiceArguments):
    """function to move chapters into corresponding subdirectory folders as volumes"""
    directory_in = args.directory_in
    directory_out = args.directory_out

    chapters = get_files(path=directory_in)
    mapping = create_mapping_chapters_to_vols()
    move_chapters_to_volumes(directory_out, chapters, mapping)


def main(args: ServiceArguments):
    """main function for organizing files feature"""

    organize_chapters_to_vol(args)
