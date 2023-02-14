import logging

from ECU_commands.ecu import ECU
from Interfaces.obdhandler import OBDHandler
from constants import GENERAL

logger = logging.getLogger(GENERAL)

class Coolant(ECU):
    def __init__(self) -> None:
        self.coolOBD = -99
        if 'COOLANT_TEMP' in OBDHandler.commands:
            logger.info('Coolant supported')
            OBDHandler.attach(self)
            self.coolOBD = OBDHandler.commands['COOLANT_TEMP']

    def update(self, commands):
        logger.debug('Getting coolant temps')
        self.coolOBD = commands["COOLANT_TEMP"]

    def print(self):
        return 'Temp: ' + str(self.coolOBD) + ' C'
