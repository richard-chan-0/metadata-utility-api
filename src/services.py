import src.rename_media.rename_media as RenameService
from src.organize_media.organize_chapters_to_vol import (
    main as organize_chapters_to_vol,
)
from src.rezip_cbz_files.rezip_chapters_to_vol import (
    main as rezip_chapters_to_vol,
)
from src.prepare_for_jellyfin.prepare_for_jellyfin import main as prepare_for_jellyfin
from src.create_volumes.create_volumes import create_volumes
from src.data_types.ServiceMetaData import ServiceMetaData
from src.exceptions.exceptions import InvalidService
from typing import Iterable
from src.data_types.service_constants import *

IMAGES_IN = "images_in"
IMAGES_OUT = "images_out"


def get_list_service() -> Iterable[str]:
    """function to get list of service names"""
    return [key for key in get_services().keys()]


def get_services() -> dict[str, ServiceMetaData]:
    """returns mapping of service names to service metadata"""
    return {
        **RenameService.rename_services,
        ORGANIZE_CHAPTERS_TO_VOL_NAME: ServiceMetaData(
            "chapter_pdf_in", "chapter_pdf_out", organize_chapters_to_vol
        ),
        REZIP_CHAPTERS_TO_VOL_NAME: ServiceMetaData(
            "chapter_zip_in", "chapter_zip_out", rezip_chapters_to_vol
        ),
        CREATE_VOLUMES_NAME: ServiceMetaData(None, None, create_volumes),
        "ffmpeg": ServiceMetaData(None, None, None),
    }


def return_service(service_name: str) -> ServiceMetaData:
    """returns service"""
    services = get_services()

    if service_name not in services:
        raise InvalidService(f"{service_name} is not valid service")

    return services[service_name]
