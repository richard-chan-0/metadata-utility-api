import os
import json
from pathlib import Path
from typing import List
from src.lib.exceptions.exceptions import FileSystemError
from src.lib.utilities.os_functions import is_dir
import logging

logger = logging.getLogger(__name__)


def validate_query_path(path):
    """Validate the provided query path.

    Args:
        path (str): The path to validate.

    Raises:
        FileSystemError: If the path is not a valid directory.
    """
    if not path:
        logger.info("No path provided, skipping validation.")
        return

    with open("allowed_paths.json", "r") as f:
        data = json.load(f)
        allowed_paths = data.get("allowed_paths", [])
        logger.info(f"Allowed paths: {allowed_paths}")
        for allowed_path in allowed_paths:
            logger.info(
                f"Checking if path '{path}' starts with allowed path '{allowed_path}'"
            )
            if not path.startswith(allowed_path):
                continue

            if not is_dir(path):
                logger.info(f"Path '{path}' is not a valid directory.")
                raise FileSystemError(f"Path '{path}' is not a valid directory.")

            logger.info(f"Path '{path}' is valid.")
            return

        raise FileSystemError(f"Path '{path}' is not within allowed paths.")
