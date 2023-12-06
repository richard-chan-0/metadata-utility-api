import src.rename_media.name_functions as NameFunctions
from src.exceptions.exceptions import RenameMediaError
from src.factories.factories import create_file
from pytest import raises


def test_numbers_less_than_three_digits_has_zeros():
    test_number = 3
    result = NameFunctions.prepend_zeros(test_number)
    assert result == "003"


def test_numbers_more_than_three_digits_returns_same_number():
    test_number = 3141

    result = NameFunctions.prepend_zeros(test_number)

    assert result == "3141"


def test_name_produces_correct_file_name():
    story = "Spy x Family"
    chapter = "2"
    page = 1

    result = NameFunctions.create_calibre_image_name(story, chapter, page)

    assert result == "Spy x Family - c002 - p001.png"


def test_create_jellyfin_episode_name_happy_path():
    season_number = 1
    episode_number = 1
    expected = "Episode S01E01.mkv"

    result = NameFunctions.create_jellyfin_episode_name(season_number, episode_number)

    assert result == expected


def test_create_jellyfin_episode_name_raise_error_for_negative():
    season_number = -1
    episode_number = 1

    with raises(RenameMediaError):
        NameFunctions.create_jellyfin_episode_name(season_number, episode_number)


def test_cleanup_filename_removes_all_text_in_parenthesis():
    story_name = "some media"
    dirty_string = "some media (2023) (abc) (1980x300).jpg"
    cleaned_string = "some media-some media.jpg"
    test_file = create_file(dirty_string, "")

    result = NameFunctions.cleanup_filename(story_name, test_file)

    assert result == cleaned_string
