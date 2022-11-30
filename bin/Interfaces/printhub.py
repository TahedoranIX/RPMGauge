from abc import ABC, abstractmethod

class PrintHub(ABC):
    @abstractmethod
    def print(self, text):
        pass