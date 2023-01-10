from constants import WAIT_TIME_PRINTHUB, WAIT_RESET_GAS
from lib.RotaryLibrary.encoder import Encoder
from obdsingle import OBDSingle
from ECU_commands.ecu import ECU
from Observers.observable import Observable


class DtcScreen(ECU):
    def __init__(self) -> None:
        super().__init__()
        self.dtcCodes = OBDSingle.commands["dtc"]
        self.actualCode = 0  # Actual code we're looking in.
        self.clearCounter = 0

    def update(self, commands: Observable):
        if len(self.dtcCodes):
            self.checkMenuCode()
            self.cleanCodes()

    def checkMenuCode(self):
        if Encoder.getButtonValue():
            self.actualCode += 1
            self.actualCode = self.actualCode % len(self.dtcCodes)

    def checkCleanButton(self):
        if Encoder.getButtonValue():
            self.clearCounter += WAIT_TIME_PRINTHUB
        else:
            self.clearCounter = 0

    def cleanCodes(self):
        self.checkCleanButton()
        if self.clearCounter >= WAIT_RESET_GAS:
            self.clearCounter = 0
            OBDSingle.clearCodes()
            self.dtcCodes = OBDSingle.commands["dtc"]

    def checkDtc(self):
        if len(self.dtcCodes):
            code = self.dtcCodes[self.actualCode][1]
            if code == "":
                return "Vehicle-specific code"
            return code
        else:
            return "No ML codes"

    def print(self):
        return self.checkDtc()
