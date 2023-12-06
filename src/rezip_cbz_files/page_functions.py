from zipfile import ZipFile
import src.utilities.os_functions as SystemUtilities
import logging
from src.data_types.DirectoryFile import DirectoryFile
from typing import Iterable

logger = logging.getLogger(__name__)


def extract_pages_from_chapter(directory_in: str, chapters: Iterable[DirectoryFile]):
    """function to extract all page files from chapter files"""
    logger.info("unzipping pages from chapter file: %s", chapter.name)
    for chapter in chapters:
        if SystemUtilities.is_compressed(chapter.name):
            with ZipFile(chapter, "r") as zip:
                zip.extractall(directory_in)


def move_pages_to_temp(directory_in: str, temp_path: str):
    """function to move pages into temp folder"""
    logger.info("migrating page files into temporary folder")
    images = SystemUtilities.get_images(directory_in)

    return SystemUtilities.move_files(images, temp_path)
