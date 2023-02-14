import logging
import time
from typing import List

from constants import WAIT_REFRESH_OBD, GASOLINE_DENSITY, GASOLINE_STOICHIOMETRIC, DIESEL_DENSITY, \
    DIESEL_STOICHIOMETRIC, GENERAL
from lib.RotaryLibrary.encoder import Encoder
from Interfaces.printhub import PrintHub
from menu import Menu
logger = logging.getLogger(GENERAL)

class Car:
    density = GASOLINE_DENSITY
    stoichiometric = GASOLINE_STOICHIOMETRIC

    def __init__(self, encoder, display, menus):
        self.encoder: Encoder = encoder
        self.printHub: PrintHub = display
        self.menuList: List[Menu] = menus

    def dieselCar(self):
        Car.density = DIESEL_DENSITY
        Car.stoichiometric = DIESEL_STOICHIOMETRIC

    def mainLoop(self):
        try:
            menu = 0
            while True:
                self.printHub.print(self.menuList[menu].print())
                menu = self.encoder.getRotaryValue() % len(self.menuList)

        except Exception as e:
            print(e)
            time.sleep(WAIT_REFRESH_OBD * 5)
            self.mainLoop()
