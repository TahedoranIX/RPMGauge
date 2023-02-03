import time
from typing import List

from constants import WAIT_REFRESH_OBD
from lib.RotaryLibrary.encoder import Encoder
from Interfaces.printhub import PrintHub
from menu import Menu
import keyboard


class Car:
    def __init__(self, encoder, display, menus):
        self.encoder: Encoder = encoder
        self.printHub: PrintHub = display
        self.menuList: List[Menu] = menus

    def mainLoop(self):
        try:
            menu = 0
            while True:
                #TODO: QUITAR LA COMPROBACIÓN DEL TECLADO PARA PASAR DE MENUS
                # pip uninstall keyboard
                self.printHub.print(self.menuList[menu].print())
                menu += keyboard.is_pressed('up')
                menu = menu % len(self.menuList)
                # menu = self.encoder.getRotaryValue() % len(self.menuList)
        except Exception as e:
            print(e)
            time.sleep(WAIT_REFRESH_OBD * 5)
            self.mainLoop()
