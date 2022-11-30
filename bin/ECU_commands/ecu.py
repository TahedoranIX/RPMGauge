from abc import ABC, abstractmethod

from Observers.observable import Observable
from Observers.observer import Observer

MINIMUM_SPEED = 5


class ECU(Observer, ABC):
    @abstractmethod
    def update(self, commands: Observable):
        pass

    @abstractmethod
    def print(self) -> None:
        pass
