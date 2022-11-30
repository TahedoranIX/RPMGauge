from abc import ABC, abstractmethod


from Observers.observable import Observable
from Observers.observer import Observer
from obdsingle import OBDSingle

MINIMUM_SPEED = 5


class ECU(Observer, ABC):
    def __init__(self) -> None:
        OBDSingle.attach(self)
    @abstractmethod
    def update(self, commands: Observable):
        pass

    @abstractmethod
    def print(self) -> None:
        pass
