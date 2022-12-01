import time

from Interfaces.printhub import PrintHub
from constants import WAIT_TIME
from lib.LCDLibrary.lcdLibrary import LCD


class LCDSingle(PrintHub, object):
    lcd = None
    @classmethod
    def __init__(cls, d4=None, d5=None, d6=None, d7=None, en=None, rs=None):
        cls.lcd = LCD(d4, d5, d6, d7, en, rs)

    @classmethod
    def print(cls, text):
        cls.lcd.clearDisplay()
        cls.lcd.writeMessage(text[0]+'\n'+text[1])
        time.sleep(WAIT_TIME)

