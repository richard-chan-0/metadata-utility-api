from abc import ABC, abstractmethod


class Gui(ABC):
    @abstractmethod
    def start():
        pass
