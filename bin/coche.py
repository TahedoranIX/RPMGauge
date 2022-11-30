from typing import List

from lib.RotaryLibrary.encoder import Encoder
from menu import Menu
class Coche:
    def __init__(self, encoder, display, menus):
        self.encoder = encoder
        self.printHub = display
        self.menuList: List[Menu] = menus

    def print(self, text):
        self.printHub.print(text)
