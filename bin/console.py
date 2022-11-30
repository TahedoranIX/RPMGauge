from PrintHub import PrintHub
from Utils.Singleton import SingletonMeta


class Console(metaclass=SingletonMeta, PrintHub):
    def print(self, text):
        for i in text:
            print(i)
            print("\n")
