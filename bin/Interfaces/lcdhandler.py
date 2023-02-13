import time
from typing import List

from Interfaces.printhub import PrintHub
from constants import WAIT_REFRESH_PRINTHUB
from lib.LCDLibrary.lcd import LCD


class LCDHandler(PrintHub, object):
    lcd = None

    @classmethod
    def __init__(cls, d4, d5, d6, d7, en, rs):
        cls.lcd = LCD(d4, d5, d6, d7, en, rs)

    @classmethod
    def print(cls, text):
        cls.lcd.clearDisplay()
        if not isinstance(text, List):
            cls.lcd.writeMessage(text)
        else:
            if len(text) > 1:
                cls.lcd.writeMessage(text[0] + '\n' + text[1])
            else:
                cls.lcd.writeMessage(text[0])
        time.sleep(WAIT_REFRESH_PRINTHUB)
