from abc import ABC, abstractmethod

from Observers.observable import Observable
from Observers.observer import Observer
from Interfaces.obdhandler import OBDHandler


class ECU(Observer, ABC):
	def __init__(self) -> None:
		OBDHandler.attach(self)

	@abstractmethod
	def update(self, commands: Observable):
		pass

	@abstractmethod
	def print(self) -> None:
		pass
