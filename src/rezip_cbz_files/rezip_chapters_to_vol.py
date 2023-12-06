from zipfile import ZipFile
import src.utilities.os_functions as SystemUtilities
from src.exceptions.exceptions import RezipChaptersToVolError
from src.rezip_cbz_files.page_functions import (
    extract_pages_from_chapter,
    move_pages_to_temp,
)
import logging
from src.data_types.DirectoryFile import DirectoryFile
from src.data_types.ServiceArguments import ServiceArguments
from typing import Iterable

logger = logging.getLogger(__name__)
TEMP_FOLDER = "temp"


def create_volume_from_pages(
    pages: Iterable[DirectoryFile], directory_out: str, volume_name: str
):
    """function to create volume from page files"""
    logger.info("zipping pages into volume")
    volume_path = SystemUtilities.create_new_file_path(directory_out, volume_name)
    with ZipFile(volume_path, "w") as volume:
        for page in pages:
            try:
                volume.write(page)
            except Exception as err:
                raise RezipChaptersToVolError(err)

    logger.info("volume created with path %s", volume_path)
    return volume_path


def clean_system(temp_path: str, chapters: Iterable[DirectoryFile]):
    """function to clean files after creating volume file"""
    logger.info("removing temporary folder")
    SystemUtilities.remove_directory(temp_path)

    logger.info("removing chapter files from directory")
    for chapter in chapters:
        SystemUtilities.remove_file(chapter.path)

    logger.info("app folders are cleaned")


def rezip_chapters_to_vol(args, volume_name: str = "temp.cbz"):
    """function that processes multiple cbz files into single cbz file"""
    directory_in = args.directory_in
    directory_out = args.directory_out

    logger.info("creating volume file: %s", volume_name)
    chapters = SystemUtilities.get_files(directory_in)
    temp_path = SystemUtilities.create_sub_directory(directory_in, TEMP_FOLDER)

    logger.info("collecting pages from chapter files")
    extract_pages_from_chapter(directory_in, chapters)
    pages = move_pages_to_temp(directory_in, temp_path)

    volume_path = create_volume_from_pages(pages, directory_out, volume_name)
    print(f"pages written to volume: {volume_path}")

    clean_system(temp_path, chapters)


def main(args: ServiceArguments):
    """service to open list of zip files and compile them into single zip file"""
    rezip_chapters_to_vol(args)
