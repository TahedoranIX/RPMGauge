from constants import TICK_CLEAN_CODES, WAIT_CLEAN_CODES
from lib.RotaryLibrary.encoder import Encoder
from Interfaces.obdhandler import OBDHandler
from ECU_commands.ecu import ECU


class DtcScreen(ECU):
    def __init__(self) -> None:
        self.dtcCodes = OBDHandler.commands['GET_DTC']
        self.actualCode = 0  # Actual code we're looking in.
        self.clearCounter = 0

    def update(self, commands):
        pass

    def navigateInCodes(self):
        if Encoder.getButtonValue():
            self.actualCode += 1
            self.actualCode = self.actualCode % len(self.dtcCodes)

    def checkCleanButton(self):
        self.clearCounter = TICK_CLEAN_CODES + self.clearCounter if Encoder.getButtonValue() else 0

    def cleanCodes(self):
        self.checkCleanButton()
        if self.clearCounter >= WAIT_CLEAN_CODES:
            self.clearCounter = 0
            OBDHandler.clearCodes()
            self.dtcCodes = OBDHandler.commands["GET_DTC"]

    def checkDtc(self):
        actualCode = "No ML codes"
        if len(self.dtcCodes):
            self.navigateInCodes()
            code = self.dtcCodes[self.actualCode][1]
            if code == "":  # Library doesn't know how to describe this code.
                actualCode = "Vehicle-specific code"
            else:
                actualCode = code
            self.cleanCodes()
        return str(actualCode)

    def print(self):
        return self.checkDtc()
