import logging

from constants import TICK_CLEAN_CODES, WAIT_CLEAN_CODES, GENERAL
from lib.RotaryLibrary.encoder import Encoder
from Interfaces.obdhandler import OBDHandler
from ECU_commands.ecu import ECU

logger = logging.getLogger(GENERAL)

class DtcScreen(ECU):
    def __init__(self) -> None:
        self.dtcCodes = OBDHandler.commands['GET_DTC']
        self.actualCode = 0  # Actual code we're looking in.
        self.clearCounter = 0

    def update(self, commands):
        pass

    def navigateInCodes(self):
        if Encoder.getButtonValue():
            logger.debug('DTC - Navigating in codes.')
            self.actualCode += 1
            self.actualCode = self.actualCode % len(self.dtcCodes)

    def checkCleanButton(self):
        self.clearCounter = TICK_CLEAN_CODES + self.clearCounter if Encoder.getButtonValue() else 0
        logger.debug('DTC - Tick count cleaning process: ' + str(self.clearCounter))

    def cleanCodes(self):
        self.checkCleanButton()
        if self.clearCounter >= WAIT_CLEAN_CODES:
            logger.info('DTC - Cleaning dtc codes.')
            self.clearCounter = 0
            OBDHandler.clearCodes()
            self.dtcCodes = OBDHandler.commands["GET_DTC"]

    def checkDtc(self):
        actualCode = "No ML codes"
        if len(self.dtcCodes):
            self.navigateInCodes()
            actualCode = self.dtcCodes[self.actualCode][1]
            if actualCode == "":  # Library doesn't know how to describe this code.
                actualCode = self.dtcCodes[self.actualCode][0]
            self.cleanCodes()
        return str(actualCode)

    def print(self):
        return self.checkDtc()
