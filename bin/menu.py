from abc import ABC, abstractmethod


class Menu(ABC):
    @abstractmethod
    def print(self) -> None:
        pass
