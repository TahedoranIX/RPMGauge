from typing import List

from ECU_commands.ecu import ECU


class Menu:

    def __init__(self, ecu1, ecu2):
        self.ecuList : List[ECU] = [ecu1, ecu2]

    def print(self):
        return [self.ecuList[0].print(), self.ecuList[1].print()]

