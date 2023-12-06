from tkinter import *
from tkinter.messagebox import askokcancel
from tkinter.scrolledtext import ScrolledText
from typing import Iterable, Tuple, Callable

COLUMN_COMPONENT = "1"

DEFAULT_PADDINGY = 5
DEFAULT_PADDINGX = 5
DEFAULT_DROPMENU_WIDTH = "30"
DEFUALT_BUTTON_WIDTH = "15"
DEFAULT_LABEL_WIDTH = "15"


def get_widget_value(widget: Variable):
    """function to get the value of tkinter variable"""
    return "" if not widget else widget.get()


def create_dropdown(
    root: Tk, options: Iterable[str], row_position: int, command: Callable
) -> Tuple[Variable, Widget]:
    """function to create tkinter dropdown menu"""
    dropdown_option = StringVar()
    dropdown_option.set("Select an item")
    dropdown_menu = OptionMenu(root, dropdown_option, *options, command=command)
    dropdown_menu.config(width=DEFAULT_DROPMENU_WIDTH)
    dropdown_menu.grid(
        row=row_position,
        column=COLUMN_COMPONENT,
        pady=DEFAULT_PADDINGY,
        sticky=W,
    )
    return (dropdown_option, dropdown_menu)


def create_buttoon(
    root: Tk,
    button_text: str,
    action: Callable,
    row_position: str,
    col_position: int,
    options: dict = {},
):
    """function to create a tkinter button"""
    button_options = {**options, "width": DEFUALT_BUTTON_WIDTH}
    button = Button(root, text=button_text, default="active", command=action)
    button.configure(**button_options)
    button.grid(row=row_position, column=col_position, sticky=W)
    return button


def create_label(
    root: Tk,
    text: str,
    row: str,
    options: dict = {},
    column: str = "0",
):
    """function to create tkinter label"""
    label_options = {**options, "width": DEFAULT_LABEL_WIDTH, "anchor": "w"}
    label = Label(root, text=text)
    label.configure(**label_options)
    label.grid(
        row=row, column=column, padx=DEFAULT_PADDINGX, pady=DEFAULT_PADDINGY, sticky=W
    )
    return label


def create_frame(
    root: Tk,
    row: str,
    column: str,
    options: dict = {},
):
    """function to create tkinter label"""
    frame = Frame(root)
    frame.configure(**options)
    frame.grid(row=row, column=column, sticky=NSEW)
    return frame


def create_confirmation_window(title, message):
    """function to create a message box to give confiramation window"""
    return askokcancel(title=title, message=message)


def create_console_textbox(root: Tk, options: dict, row: str, col: str):
    """function to create a read-only textbox"""
    console = ScrolledText(root, **options)
    console.configure(state="disabled")
    console.grid(
        row=row, column=col, padx=DEFAULT_PADDINGX, pady=DEFAULT_PADDINGY, sticky=W
    )
    return console


def destroy_widgets(widgets: Iterable[Widget]):
    """function to destroy widgets"""
    for widget in widgets:
        if widget:
            widget.destroy()


def create_input_field(root: Tk, row_position: str) -> Tuple[Variable, Widget]:
    """function to create tkinter input field"""
    input_field_text = StringVar()
    entry = Entry(root, textvariable=input_field_text, width=DEFAULT_DROPMENU_WIDTH)
    entry.grid(row=row_position, column=COLUMN_COMPONENT, sticky=W)
    return (input_field_text, entry)
