from typing import List

from lib.RotaryLibrary.encoder import Encoder
from printhub import PrintHub
from threading import Thread
from menu import Menu


class Coche:
    def __init__(self, encoder, display, menus):
        self.encoder : Encoder = encoder
        self.printHub : PrintHub = display
        self.menuList: List[Menu] = menus

    def print(self, text):
        self.printHub.print(text)

    def mainLoop(self):
        menu = 0
        while True:
            thread = Thread(target=self.printHub.print(self.menuList[menu].print()))
            thread.start()
            # menu = self.encoder.getValue() % len(self.menuList)
            thread.join()