from src.tkinter.gui import Gui
from src.data_types.service_constants import *
from src.tkinter.rename_videos_gui import RenameVideosGui
from src.tkinter.rename_comics_gui import RenameComicsGui
from src.tkinter.ffmpeg_gui import FfmpegGui
from src.exceptions.exceptions import InvalidService


def get_services_gui() -> Gui:
    """returns mapping of service names to service metadata"""
    return {
        RENAME_FILES_TO_JELLY_EPISODES: RenameVideosGui,
        RENAME_FILES_TO_JELLY_COMICS: RenameComicsGui,
        "ffmpeg": FfmpegGui,
    }


def return_gui(service_name: str) -> Gui:
    """returns service"""
    services = get_services_gui()

    if service_name not in services:
        raise InvalidService(f"{service_name} is not valid service")

    return services[service_name]
