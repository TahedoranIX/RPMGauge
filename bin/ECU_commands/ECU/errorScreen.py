from constants import WAIT_TIME_PRINTHUB, WAIT_RESET_GAS
from lib.RotaryLibrary.encoder import Encoder
from obdsingle import OBDSingle
from ECU_commands.ecu import ECU
from Observers.observable import Observable


class Coolant(ECU):
    def __init__(self) -> None:
        super().__init__()
        self.dtcCodes = OBDSingle.commands["dtc"]
        self.actualCode = 0  # Actual code we're looking in.
        self.clearCounter = 0

    def update(self, commands: Observable):
        self.checkButton()
        self.cleanCodes()

    def checkButton(self):
        if Encoder.getButtonValue():
            self.actualCode += 1
            self.actualCode = self.actualCode % len(self.dtcCodes)

    def cleanCodes(self):
        if Encoder.getButtonValue():
            self.clearCounter += WAIT_TIME_PRINTHUB
        if self.clearCounter == WAIT_RESET_GAS:
            self.clearCounter = 0
            OBDSingle.clearCodes()

    def checkDtc(self):
        code = self.dtcCodes[self.actualCode][1]
        if code == "":
            return "Vehicle-specific code"
        return code

    def print(self):
        return self.checkDtc()
