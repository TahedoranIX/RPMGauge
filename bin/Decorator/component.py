from abc import ABC, abstractmethod
from menu import Menu


class Component(ABC, Menu):

    @abstractmethod
    def print(self) -> None:
        pass
