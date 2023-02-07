from ECU_commands.ecu import ECU
from Interfaces.obdhandler import OBDHandler


class Coolant(ECU):
    def __init__(self) -> None:
        self.coolOBD = -99
        if 'COOLANT_TEMP' in OBDHandler.commands:
            OBDHandler.attach(self)
            self.coolOBD = OBDHandler.commands['COOLANT_TEMP']

    def update(self, commands):
        self.coolOBD = int(commands["COOLANT_TEMP"])

    def print(self):
        return 'Temp: ' + str(self.coolOBD) + ' C'
