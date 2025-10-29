import pytest
import json
import tempfile
import os
from unittest.mock import patch, mock_open
from src.lib.utilities.path_validator import validate_query_path
from src.lib.exceptions.exceptions import FileSystemError


@pytest.fixture
def mock_allowed_paths_single():
    """Mock allowed_paths.json with a single allowed path"""
    return json.dumps({"allowed_paths": ["/tmp/allowed"]})


@pytest.fixture
def mock_allowed_paths_multiple():
    """Mock allowed_paths.json with multiple allowed paths"""
    return json.dumps({"allowed_paths": ["/tmp/allowed1", "/tmp/allowed2"]})


@pytest.fixture
def temp_directory():
    """Create a temporary directory for testing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


def test_validate_query_path_none():
    """Test that None path is allowed (skips validation)"""
    # Should not raise any exception
    validate_query_path(None)


def test_validate_query_path_empty_string():
    """Test that empty string path is allowed (skips validation)"""
    # Should not raise any exception
    validate_query_path("")


@patch("builtins.open", new_callable=mock_open)
def test_validate_query_path_valid_directory(
    mock_file, mock_allowed_paths_single, temp_directory
):
    """Test validation with valid directory that starts with allowed path"""
    mock_file.return_value.read.return_value = mock_allowed_paths_single

    # Create a subdirectory in temp_directory
    test_path = os.path.join(temp_directory, "subdir")
    os.makedirs(test_path)

    # Mock the allowed path to be temp_directory
    mock_data = json.dumps({"allowed_paths": [temp_directory]})
    with patch("builtins.open", mock_open(read_data=mock_data)):
        # Should not raise exception
        validate_query_path(test_path)


@patch("builtins.open", new_callable=mock_open)
def test_validate_query_path_not_starting_with_allowed(
    mock_file, mock_allowed_paths_single
):
    """Test that path not starting with allowed path raises error"""
    mock_file.return_value.read.return_value = mock_allowed_paths_single

    with pytest.raises(FileSystemError) as exc_info:
        validate_query_path("/different/path")

    assert "is not within allowed paths" in str(exc_info.value)


@patch("builtins.open", new_callable=mock_open)
def test_validate_query_path_not_a_directory(mock_file, temp_directory):
    """Test that file path (not directory) raises error"""
    # Create a file in temp directory
    test_file = os.path.join(temp_directory, "test.mkv")

    # Need to use real open for file creation, then mock for config read
    import builtins

    real_open = builtins.open

    with real_open(test_file, "w") as f:
        f.write("test")

    mock_data = json.dumps({"allowed_paths": [temp_directory]})

    def side_effect_open(filename, *args, **kwargs):
        if filename == "allowed_paths.json":
            return mock_open(read_data=mock_data)()
        return real_open(filename, *args, **kwargs)

    with patch("builtins.open", side_effect=side_effect_open):
        with pytest.raises(FileSystemError) as exc_info:
            validate_query_path(test_file)

        # is_dir checks existence first, so will get "path does not exist" if file doesn't exist
        # or the validation error if it's a file not a directory
        assert "is not a valid directory" in str(
            exc_info.value
        ) or "path does not exist" in str(exc_info.value)


@patch("builtins.open", new_callable=mock_open)
def test_validate_query_path_nonexistent_directory(mock_file, temp_directory):
    """Test that nonexistent path raises error from is_dir check"""
    nonexistent = os.path.join(temp_directory, "does_not_exist")

    mock_data = json.dumps({"allowed_paths": [temp_directory]})
    with patch("builtins.open", mock_open(read_data=mock_data)):
        with pytest.raises(FileSystemError):
            validate_query_path(nonexistent)


@patch("builtins.open", new_callable=mock_open)
def test_validate_query_path_nested_subdirectory(mock_file, temp_directory):
    """Test validation with nested subdirectory structure"""
    # Create nested structure: temp_directory/show/Season 01
    nested_path = os.path.join(temp_directory, "show", "Season 01")
    os.makedirs(nested_path)

    mock_data = json.dumps({"allowed_paths": [temp_directory]})
    with patch("builtins.open", mock_open(read_data=mock_data)):
        # Should not raise exception
        validate_query_path(nested_path)


@patch("builtins.open", new_callable=mock_open)
def test_validate_query_path_exact_allowed_path(mock_file, temp_directory):
    """Test validation with exact allowed path"""
    mock_data = json.dumps({"allowed_paths": [temp_directory]})
    with patch("builtins.open", mock_open(read_data=mock_data)):
        # Should not raise exception
        validate_query_path(temp_directory)


def test_validate_query_path_missing_config_file():
    """Test that missing config file raises error"""
    # Mock open to raise FileNotFoundError when trying to read config
    with patch("builtins.open", side_effect=FileNotFoundError("Config not found")):
        with pytest.raises(FileNotFoundError):
            validate_query_path("/some/path")


@patch("builtins.open", new_callable=mock_open)
def test_validate_query_path_invalid_json(mock_file):
    """Test that invalid JSON in config raises error"""
    mock_file.return_value.read.return_value = "invalid json{"

    with pytest.raises(json.JSONDecodeError):
        validate_query_path("/some/path")


@patch("builtins.open", new_callable=mock_open)
def test_validate_query_path_empty_allowed_paths(mock_file):
    """Test validation with empty allowed_paths list"""
    mock_data = json.dumps({"allowed_paths": []})
    with patch("builtins.open", mock_open(read_data=mock_data)):
        # Should return without error since loop doesn't execute
        validate_query_path("")


@patch("builtins.open", new_callable=mock_open)
def test_validate_query_path_multiple_allowed_first_matches(mock_file, temp_directory):
    """Test with multiple allowed paths where first one matches"""
    subdir = os.path.join(temp_directory, "media")
    os.makedirs(subdir)

    mock_data = json.dumps({"allowed_paths": [temp_directory, "/other/path"]})
    with patch("builtins.open", mock_open(read_data=mock_data)):
        # Should not raise exception - first path matches
        validate_query_path(subdir)
