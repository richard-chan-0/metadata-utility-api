from typing import Iterable


class FfmpegCommand:
    __command: Iterable[str] = []

    def __init__(self):
        pass

    def __init__(self, command):
        self.__command = command

    def __str__(self):
        return " ".join(self.__command)
