from src.tkinter.rename_gui import RenameGui
from src.tkinter.tkinter_functions import *
from src.rename_media.rename_media import rename_files
from src.data_types.service_constants import RENAME_FILES_TO_JELLY_COMICS
from src.factories.factories import create_basic_service_args
from tkinter import *
from logging import getLogger
from json import dumps

logger = getLogger(__name__)


class RenameComicsGui:
    def __init__(self, root: Tk):
        self.__root = root
        self.__root.title("Rename Comics Utility")
        self.__base_gui = RenameGui(root)

        self.__story_name_text = None
        self.__story_name_row = 2
        self.__submit_button_row = 5

        self.__story_name_text = None

        self.__rename_mapping = None

    def __create_story_name_entry(self):
        """function to setup entry component to enter name for comic functions"""
        create_label(
            self.__root,
            "Enter the Story Name:",
            row=self.__story_name_row,
            options=self.__base_gui.DEFAULT_OPTIONS,
        )
        text, _ = create_input_field(self.__root, self.__story_name_row)
        self.__story_name_text = text

    def __create_rename_mapping(self):
        """function that runs rename methods"""
        logger.info("retrieving service configurations")
        service_args = create_basic_service_args(
            self.__base_gui.directory_in, self.__base_gui.directory_out
        )
        service_args.story = get_widget_value(self.__story_name_text)
        logger.info("creating name mapping")

        self.__rename_mapping = self.__base_gui.service(service_args)
        mapping = dumps(self.__rename_mapping, indent=4)
        self.__base_gui.log_to_console(mapping)

    def __create_submit_button(self, root):
        """function to create button for generating name mapping"""
        create_label(
            self.__root,
            "Run",
            row=self.__submit_button_row,
            options=self.__base_gui.DEFAULT_OPTIONS,
        )

        create_buttoon(
            root,
            button_text="Create New File Names",
            action=self.__create_rename_mapping,
            row_position=0,
            col_position=1,
            options=self.__base_gui.DEFAULT_OPTIONS,
        )

    def __create_download_button(self, root):
        create_buttoon(
            root=root,
            button_text="Pull Files?",
            action=self.__base_gui.pull_files_from_download,
            row_position=0,
            col_position=0,
            options=self.__base_gui.DEFAULT_OPTIONS,
        )

    def __create_rename_button(self, root):
        create_buttoon(
            root=root,
            button_text="Update Files",
            action=self.__update_files,
            row_position=0,
            col_position=2,
            options=self.__base_gui.DEFAULT_OPTIONS,
        )

    def __create_action_buttons(self):
        """function to create frame and couple the buttons to the frame on gui"""
        frame = create_frame(
            self.__root,
            row=self.__submit_button_row,
            column=COLUMN_COMPONENT,
            options=self.__base_gui.DEFAULT_OPTIONS,
        )
        self.__create_download_button(frame)
        self.__create_submit_button(frame)
        self.__create_rename_button(frame)

    def __add_service_widgets(self):
        self.__create_story_name_entry()
        self.__create_action_buttons()

    def __update_files(self):
        """function to rename the files"""
        is_okay = create_confirmation_window(
            "Confirmation", "Are you sure you want to rename these files?"
        )

        if not is_okay:
            self.__base_gui.log_to_console("rename files aborted!")
            return

        logger.info("updating file names in system")
        self.__base_gui.log_to_console("renaming files!")
        rename_files(rename_mapping=self.__rename_mapping)

    def start(self):
        self.__base_gui.init_gui()
        self.__base_gui.init_gui(RENAME_FILES_TO_JELLY_COMICS)
        self.__add_service_widgets()
        self.__root.mainloop()
