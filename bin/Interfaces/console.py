import time
from typing import List

from Interfaces.printhub import PrintHub
from constants import WAIT_TIME


class Console(PrintHub):

    def print(self, text):
        if isinstance(text, List):
            for i in text:
                print(i)
        else:
            print(text)
        print("\n")
        time.sleep(WAIT_TIME)
