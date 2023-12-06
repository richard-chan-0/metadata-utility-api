from dataclasses import dataclass
from typing import Callable


@dataclass
class ServiceMetaData:
    """class for holding meta data for ebook settings"""

    directory_in: str
    directory_out: str
    service: Callable
