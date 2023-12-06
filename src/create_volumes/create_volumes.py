from src.organize_media.organize_chapters_to_vol import organize_chapters_to_vol
from src.rezip_cbz_files.rezip_chapters_to_vol import rezip_chapters_to_vol
from src.data_types.ServiceArguments import ServiceArguments
from src.factories.factories import create_basic_service_args
from src.utilities.os_functions import (
    get_sub_directories,
    get_files,
    move_files,
    remove_directory,
)
import logging

logger = logging.getLogger(__name__)


def get_chapters_for_volumes(directory_in, directory_out):
    """creates volume folders and moves corresponding chapter files"""
    args = create_basic_service_args(directory_in, directory_out)

    organize_chapters_to_vol(args)

    return get_sub_directories(directory_out)


def create_volume(
    directory_in: str, directory_out: str, chaper_files_path: str, volume_name: str
):
    """function to create volume file using files in a volume directory"""
    chapters = get_files(chaper_files_path)
    args = create_basic_service_args(directory_in, directory_out)

    move_files(chapters, directory_in)
    rezip_chapters_to_vol(args, volume_name)

    remove_directory(chaper_files_path)


def create_volumes(args: ServiceArguments):
    """creates set of volume files from list of chapters"""
    chapters_in = args.directory_in
    chapters_out = args.directory_in

    volume_folders = get_chapters_for_volumes(chapters_in, chapters_out)

    volume_in = args.directory_out
    volume_out = args.directory_out

    for folder in volume_folders:
        zip_name = f"{folder.name}.cbz"
        create_volume(volume_in, volume_out, folder.path, zip_name)
