from abc import ABC, abstractmethod

from Observers.observable import Observable
from Observers.observer import Observer
from menu import Menu

MINIMUM_SPEED = 5


class ECU(ABC, Menu, Observer):
    def __init__(self):
        self.__commands = []
        self.__stopped = False


    def update(self, subject: Observable):
        self.__commands = subject.getCommands()
        if self.__commands["speed"] < MINIMUM_SPEED and not self._stopped:
            self.__stopped = True
        elif self.__commands["speed"] > MINIMUM_SPEED and self.__stopped:
            self.__stopped = False

    @abstractmethod
    def print(self) -> None:
        pass
