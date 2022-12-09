import time
from typing import List

from constants import WAIT_TIME
from lib.RotaryLibrary.encoder import Encoder
from Interfaces.printhub import PrintHub
from threading import Thread
from menu import Menu


class Coche:
    def __init__(self, encoder, display, menus):
        self.encoder : Encoder = encoder
        self.printHub : PrintHub = display
        self.menuList: List[Menu] = menus

    def mainLoop(self):
        try:
            menu = 0
            while True:
                thread = Thread(target=self.printHub.print(self.menuList[menu].print()))
                thread.start()
                menu = self.encoder.getValue() % len(self.menuList)
                thread.join()
        except Exception as e:
            print(e)
            time.sleep(WAIT_TIME*5)
            self.mainLoop()

