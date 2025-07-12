from pytest import fixture
from src.utilities.app_functions import read_dict


@fixture
def test_json():
    return {
        "attribute1": {
            "subattribute1": {"subsubattribute1": "hello"},
            "subattribute2": "world",
        },
        "attribute2": "hello world",
    }


def test_read_dict_happy_path(test_json):
    value = read_dict("attribute1.subattribute1.subsubattribute1", test_json)
    assert value == "hello"


def test_read_dict_missing_value(test_json):
    value = read_dict("attribute3", test_json)
    assert value is None


def test_read_dict_nested_missing_value(test_json):
    value = read_dict("attribute1.subattribute2.subsubattribute1", test_json)
    assert value is None
