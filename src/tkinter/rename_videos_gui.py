from src.tkinter.rename_gui import RenameGui
from src.tkinter.tkinter_functions import *
from src.data_types.service_constants import RENAME_FILES_TO_JELLY_EPISODES
from src.rename_media.rename_media import rename_files
from src.factories.factories import create_basic_service_args
from tkinter import *
from logging import getLogger
from json import dumps

logger = getLogger(__name__)


class RenameVideosGui:
    NUMERIC_OPTIONS = [i for i in range(15)]
    EXTENSION_OPTIONS = ["mkv", "ass", "default.ass", "mp4"]

    def __init__(self, root: Tk):
        self.__root = root
        self.__root.title("Rename Videos Utility")

        self.__rename_module = RenameGui(self.__root)
        self.__numeric_dropdown_row = 2
        self.__extension_dropdown_row = 3
        self.__submit_button_row = 5
        self.__start_number_row = 4

        self.__numeric_click = None
        self.__extension_click = None
        self.__start_number_text = None
        self.__rename_mapping = None

    def __create_numeric_dropdown_menu(self, root):
        click, _ = create_dropdown(
            root,
            self.NUMERIC_OPTIONS,
            self.__numeric_dropdown_row,
            command=lambda x: self.__rename_module.log_to_console(f"you selected {x}"),
        )
        self.__numeric_click = click

    def __create_extension_dropdown_menu(self, root):
        click, _ = create_dropdown(
            root,
            self.EXTENSION_OPTIONS,
            self.__extension_dropdown_row,
            command=lambda x: self.__rename_module.log_to_console(f"you selected {x}"),
        )
        self.__extension_click = click

    def __create_numeric_dropdown_component(self, root):
        create_label(
            root,
            "Volume/Season?",
            self.__numeric_dropdown_row,
            options=self.__rename_module.DEFAULT_OPTIONS,
        )
        self.__create_numeric_dropdown_menu(root)

    def __create_extension_dropdown_component(self, root):
        create_label(
            root,
            "File Output Type",
            self.__extension_dropdown_row,
            options=self.__rename_module.DEFAULT_OPTIONS,
        )
        self.__create_extension_dropdown_menu(root)

    def __create_rename_mapping(self):
        """function that runs rename methods"""
        logger.info("retrieving service configurations")
        service_args = create_basic_service_args(
            self.__rename_module.directory_in, self.__rename_module.directory_out
        )
        service_args.season_number = get_widget_value(self.__numeric_click)
        service_args.extension = get_widget_value(self.__extension_click)
        service_args.start_number = get_widget_value(self.__start_number_text)
        logger.info("creating name mapping")

        self.__rename_mapping = self.__rename_module.service(service_args)
        mapping = dumps(self.__rename_mapping, indent=4)
        self.__rename_module.log_to_console(mapping)

    def __create_optional_start_entry(self, root):
        """function to setup entry component for entering path of download folder"""
        create_label(
            root,
            "Start Number:",
            row=self.__start_number_row,
            options=self.__rename_module.DEFAULT_OPTIONS,
        )

        text, _ = create_input_field(self.__root, self.__start_number_row)
        self.__start_number_text = text

    def __create_submit_button(self, root):
        """function to create button for generating name mapping"""

        create_buttoon(
            root,
            button_text="Create New File Names",
            action=self.__create_rename_mapping,
            row_position=0,
            col_position=1,
            options=self.__rename_module.DEFAULT_OPTIONS,
        )

    def __create_download_button(self, root):
        create_buttoon(
            root=root,
            button_text="Pull Files?",
            action=self.__rename_module.pull_files_from_download,
            row_position=0,
            col_position=0,
            options=self.__rename_module.DEFAULT_OPTIONS,
        )

    def __create_rename_button(self, root):
        create_buttoon(
            root=root,
            button_text="Update Files",
            action=self.__update_files,
            row_position=0,
            col_position=2,
            options=self.__rename_module.DEFAULT_OPTIONS,
        )

    def __create_action_buttons(self, root):
        """function to create frame and couple the buttons to the frame on gui"""
        create_label(
            self.__root,
            "Run",
            row=self.__submit_button_row,
            options=self.__rename_module.DEFAULT_OPTIONS,
        )
        frame = create_frame(
            root,
            row=self.__submit_button_row,
            column=COLUMN_COMPONENT,
            options=self.__rename_module.DEFAULT_OPTIONS,
        )
        self.__create_download_button(frame)
        self.__create_submit_button(frame)
        self.__create_rename_button(frame)

    def __add_service_widgets(self):
        self.__create_numeric_dropdown_component(self.__root)
        self.__create_extension_dropdown_component(self.__root)
        self.__create_optional_start_entry(self.__root)

        self.__create_action_buttons(self.__root)

    def __update_files(self):
        """function to rename the files"""
        is_okay = create_confirmation_window(
            "Confirmation", "Are you sure you want to rename these files?"
        )

        if not is_okay:
            self.__rename_module.log_to_console("rename files aborted!")
            return

        logger.info("updating file names in system")
        self.__rename_module.log_to_console("renaming files!")
        rename_files(rename_mapping=self.__rename_mapping)

    def __create_window(self):
        width = 900
        height = 450
        dimension = f"{width}x{height}"
        self.__root.geometry(dimension)
        self.__root.configure(bg=RenameGui.BACKGROUND_COLOR)

    def start(self):
        self.__create_window()
        self.__rename_module.init_gui(RENAME_FILES_TO_JELLY_EPISODES)
        self.__add_service_widgets()
        self.__root.mainloop()
