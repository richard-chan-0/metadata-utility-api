from src.exceptions.exceptions import ServiceError
from src.ffmpeg.ffmpeg_functions import (
    parse_streams,
    create_options,
    get_media_streams,
    build_command,
    get_matching_stream_numbers,
)
from src.tkinter.tkinter_functions import (
    get_widget_value,
    create_confirmation_window,
    get_language_widget_details,
)
from src.utilities.os_functions import run_shell_command, get_files


def set_streams(file_entry_text, log_to_console):
    path = get_widget_value(file_entry_text)
    try:
        streams = get_media_streams(path)
    except ServiceError as se:
        log_to_console(se)
        return

    stream_objs = parse_streams(streams)
    subtitles_list = create_options(stream_objs.get("subtitle"))
    audio_list = create_options(stream_objs.get("audio"))
    attachments_list = create_options(stream_objs.get("attachment"))

    return {
        "subtitles": subtitles_list,
        "audio": audio_list,
        "attachments": attachments_list,
    }


def run_ffmpeg(commands, log_to_console):
    is_okay = create_confirmation_window(
        "Confirmation", "Are you sure you want to run these commands?"
    )

    if not is_okay:
        log_to_console("ffmpeg aborted!")
        return

    for command in commands:
        run_shell_command(command.get_command())

    log_to_console("completed default reset")


def get_details_for_all_streams(language_streams):
    """function to go iterate over language streams and extract details"""
    all_language_stream_details = []
    for stream in language_streams:
        stream_number, stream_name, stream_language = get_language_widget_details(
            stream
        )
        if not stream_name and not stream_language:
            continue
        all_language_stream_details.append(
            (stream_number, stream_name, stream_language)
        )

    return all_language_stream_details


def set_bulk_commands(
    file_entry_text, default_audios, default_subtitles, log_to_console
):
    path = get_widget_value(file_entry_text)
    all_audio_details = get_details_for_all_streams(default_audios)
    all_subtitle_details = get_details_for_all_streams(default_subtitles)

    log_to_console("")
    files = get_files(path)

    if not files:
        return

    commands = [
        parse_file_to_command(
            log_to_console, all_audio_details, all_subtitle_details, file
        )
        for file in files
    ]
    return [command for command in commands if command]


def set_single_command(
    log_to_console, file_entry_text, default_audios, default_subtitles
):
    path = get_widget_value(file_entry_text)
    audio_details = get_details_for_all_streams(default_audios)
    subtitle_details = get_details_for_all_streams(default_subtitles)
    audio_numbers = [audio_number for audio_number, _, _ in audio_details]

    subtitle_numbers = [subtitle_number for subtitle_number, _, _ in subtitle_details]
    if not audio_numbers or not subtitle_numbers:
        log_to_console("no values selected for conversion!")
        return

    log_to_console("")
    files = get_files(path)
    if not files:
        return
    file = files[0]
    log_to_console(f"building command for file {file.name}", is_clear=False)
    command = build_command(
        file_path=file.path,
        audios=audio_numbers,
        subtitles=subtitle_numbers,
        attachment=None,
    )
    log_to_console(command, is_clear=False)
    return [command]


def parse_file_to_command(
    log_to_console, all_audio_details, all_subtitle_details, file
):
    log_to_console(f"building command for file {file.name}", is_clear=False)
    json_streams = get_media_streams(file.path)
    media_streams = parse_streams(json_streams)

    new_audio_numbers = get_matching_stream_numbers(
        "audio", all_audio_details, media_streams
    )
    new_subtitle_numbers = get_matching_stream_numbers(
        "subtitle", all_subtitle_details, media_streams
    )

    if not new_audio_numbers or not new_subtitle_numbers:
        log_to_console(
            f"** could not find the language setting you are looking for {file.name}\n",
            is_clear=False,
        )
        return

    command = build_command(
        file_path=file.path,
        audios=new_audio_numbers,
        subtitles=new_subtitle_numbers,
        attachment=None,
    )
    log_to_console(command, is_clear=False)
    return command
