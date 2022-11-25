from typing import List
import time as t
from lib.OBDLibrary import obd
from threading import Thread
from Observers.observable import Observable
from Observers.observer import Observer
from Utils.Singleton import SingletonMeta


class OBDUtil(metaclass=SingletonMeta, Observable):

    def __init__(self):
        self.__obd = obd.OBD()
        self.__observers: List[Observer] = []
        self.__commands = {}
        self.__exit = False
        thread = Thread(target=self.tick(), args=(10,))
        thread.start()
        thread.join()

    def getCommands(self):
        return self.__commands
    def attach(self, observer: Observer) -> None:
        print("Subject: Attached an observer.")
        self.__observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self.__observers.remove(observer)

    """
    The subscription management methods.
    """

    def notify(self) -> None:
        for observer in self.__observers:
            observer.update(self)

    def __connection(self):
        pass

    def getParams(self):
        pass

    def tick(self):
        while not self.__exit:
            self.getParams()
            self.notify()
            t.sleep(2)

    def destroy(self):
        self.__exit = True


if __name__ == "__main__":
    thread = Thread(target=threaded_function, args=(10,))
    thread.start()
    thread.join()
    print("thread finished...exiting")