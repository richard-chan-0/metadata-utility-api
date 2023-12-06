import os
from subprocess import run, PIPE
from src.rename_media.name_functions import create_calibre_image_name
from typing import Iterable, Callable
from PIL import Image
from src.exceptions.exceptions import FileSystemError
from src.factories.factories import create_file
from src.data_types.DirectoryFile import DirectoryFile
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

ignore_files = [".DS_Store"]


def get_files(path: str) -> Iterable[DirectoryFile]:
    """function to get list of files from a path"""
    if not os.path.exists(path):
        raise FileSystemError(f"could not find: {path}")

    if is_file(path):
        filename = os.path.basename(path)
        file_path = os.path.normpath(path)
        return [create_file(filename, file_path)]

    with os.scandir(path) as entries:
        return [
            create_file(entry.name, entry.path)
            for entry in entries
            if os.path.isfile(entry.path) and entry.name not in ignore_files
        ]


def get_sorted_files(
    directory_in: str, sort_method=lambda entry: entry.name
) -> Iterable[DirectoryFile]:
    """function to get list of files from a directory and sort them"""
    directory_entries = get_files(directory_in)
    directory_entries.sort(key=sort_method)
    return directory_entries


def get_sub_directories(directory: str) -> Iterable[DirectoryFile]:
    """function to get list of files from a directory"""
    if not os.path.exists(directory):
        raise FileSystemError(f"could not find directory: {directory}")

    with os.scandir(directory) as entries:
        return [
            create_file(entry.name, entry.path)
            for entry in entries
            if os.path.isdir(entry.path)
        ]


def is_file_an_image(file_name: str) -> bool:
    """function to determine if file name is a image format"""
    return "png" in file_name or "jpg" in file_name


def is_compressed(file_name: str) -> bool:
    """function to determine if file name is compressed (.zip, .cbz)"""
    return ".cbz" in file_name or ".zip" in file_name


def get_images(directory: str) -> Iterable[DirectoryFile]:
    """function to get list of files from a directory with a image (jpg,png) extension"""
    return [file for file in get_files(directory) if is_file_an_image(file.name)]


def rename_page_images(
    directory_out: str, files: Iterable[DirectoryFile], name_function: Callable
):
    """rename image file in a directory"""
    story = os.getenv("STORY")
    chapter = os.getenv("CHAPTER")

    for page_number, file in enumerate(files):
        new_name = name_function(story, chapter, page_number)
        img = Image.open(file.path)
        new_path = create_new_file_path(directory_out, new_name)
        img.save(new_path)
        os.remove(file.path)


def rename_files(rename_mapping: dict[str, str]):
    for old_file_path, new_file_path in rename_mapping.items():
        os.rename(old_file_path, new_file_path)


def get_organization_file():
    """returns the env variable for the json file to organize volumes and chapters"""
    return os.getenv("ORGANIZATION_FILE")


def create_sub_directory(directory_out: str, sub_directory: str):
    """function to create a sub directory"""
    sub_directory_path = f"{directory_out}/{sub_directory}"
    if not os.path.exists(sub_directory_path):
        os.mkdir(sub_directory_path)
    return sub_directory_path


def move_file(old_path: str, new_path: str):
    """function to move a file by changing path"""
    if not os.path.exists(old_path):
        raise FileSystemError(f"could not find file with path: {old_path}")
    try:
        os.rename(old_path, new_path)
    except FileNotFoundError as err:
        logger.error(err)
        raise FileSystemError(f"could not move file to path: {new_path}")


def move_files(files_to_move: Iterable[DirectoryFile], destination_folder: str):
    """function to move several files into a single directory"""
    if not files_to_move:
        logger.info("no files given to move")
        return

    destination_paths = []

    for file in files_to_move:
        source = file.path
        destination = create_new_file_path(destination_folder, file.name)
        move_file(source, destination)
        destination_paths.append(destination)

    return destination_paths


def transfer_files(source_directory: str, destination_directory: str):
    """function to read files from source directory into destination directory"""
    source_files = get_files(source_directory)
    move_files(source_files, destination_directory)


def remove_directory(path: str):
    """function to remove directory and it's contents"""
    if not os.path.exists(path):
        raise FileSystemError(f"could not remove file: {path}")
    try:
        files = get_files(path)
        for file in files:
            os.remove(file.path)
        os.rmdir(path)
    except Exception as err:
        logger.error(err)
        raise FileExistsError(err)


def remove_file(path: str):
    """function to remove a file or directory"""
    if not os.path.exists(path):
        raise FileSystemError(f"could not remove file: {path}")
    try:
        os.remove(path)
    except Exception as err:
        logger.error(err)
        raise FileExistsError(err)


def get_env(env_var: str) -> str:
    """function to return environment variable"""
    return os.getenv(env_var)


def create_new_file_path(new_dir: str, file_name: str) -> str:
    """function to concat directory and file into new path"""
    return f"{new_dir}/{file_name}"


def run_shell_command(command: Iterable[str]):
    """runs a shell command given a list of arguments"""
    return run(command, stdout=PIPE, encoding="utf-8")


def is_dir(path: str):
    """function to determine if path is directory"""
    if not os.path.exists(path):
        raise FileExistsError("path does not exist")
    return os.path.isdir(path)


def is_file(path: str):
    """function to determine if path is directory"""
    if not os.path.exists(path):
        raise FileExistsError("path does not exist")
    return os.path.isfile(path)


def parse_path(path: str):
    """function to determine if path is directory"""
    if not os.path.exists(path):
        raise FileExistsError("path does not exist")
    return os.path.split(path)
