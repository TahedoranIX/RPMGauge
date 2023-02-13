from ECU_commands.ecu import ECU
from Interfaces.obdhandler import OBDHandler
from car import Car
from constants import THROTTLE_MINIMUM, WAIT_RESET_GAS, MINIMUM_SPEED, \
    WAIT_REFRESH_OBD, TICK_RESET_GAS, OK_O2_VOL
from FileHandler import FileHandler
from lib.RotaryLibrary.encoder import Encoder

# https://obdsoftware.force.com/s/article/How-to-read-OBDII-live-data-A-mechanic-guide
class Gas(ECU):
    def __init__(self):
        self.litersConsumed, self.km100Traveled = FileHandler.loadData()
        self.mpg = round(self.litersConsumed / self.km100Traveled, 1)
        self.instMpg = 0
        self.stopped = False
        self.savedFile = False
        self.resetCounter = 0
        if 'THROTTLE_POS' and 'SPEED' in OBDHandler.commands:
            self.commands = {
                'THROTTLE_POS': OBDHandler.commands['THROTTLE_POS'],
                'SPEED': OBDHandler.commands['SPEED'],
            }
            if 'FUEL_RATE' in OBDHandler.commands:
                self.commands['FUEL_RATE'] = OBDHandler.commands['FUEL_RATE']
                OBDHandler.attach(self)
            elif 'MAF' in OBDHandler.commands:
                self.commands['MAF'] = OBDHandler.commands['MAF']
                OBDHandler.attach(self)

        if 'O2_B1S1' in OBDHandler.commands:
            self.commands['O2_B1S1'] = OBDHandler.commands['O2_B1S1']

    def update(self, commands):
        for key in self.commands:
            self.commands[key] = commands[key]
        if int(self.commands["SPEED"]) <= MINIMUM_SPEED and not self.stopped:
            self.stopped = True
            FileHandler.saveData(self.litersConsumed, self.km100Traveled)
        elif int(self.commands["SPEED"]) > MINIMUM_SPEED and self.stopped:
            self.stopped = False
        self.calculateGas()

    def mafConversion(self):
        #TODO: NO TIENE BUENA PINTA ESTO DEL 02
        lambdaMix = (OK_O2_VOL / self.commands['O2_B1S1']) if 'O2_B1S1' in self.commands else 1
        return (self.commands["MAF"] / (
                Car.stoichiometric * lambdaMix * Car.density))  # g/s of air to L/s of gas.

    def calculateGas(self):
        if not self.stopped:
            self.km100Traveled += (self.commands["SPEED"] / 3600.0 * WAIT_REFRESH_OBD) / 100.0
            if round(self.commands["THROTTLE_POS"]) > THROTTLE_MINIMUM:
                literS = (self.commands["FUEL_RATE"] / 3600.0) if 'FUEL_RATE' in self.commands else self.mafConversion()
                self.litersConsumed += literS * WAIT_REFRESH_OBD
                self.instMpg = round(literS * 360000.0 / self.commands["SPEED"], 1)  # From L/s to L/100km
            else:
                self.instMpg = 0.0
            self.mpg = round(self.litersConsumed / self.km100Traveled, 1)  # L/100km

        else:  # If stopped, infinite consumption
            self.instMpg = '---'

    def checkButton(self):
        self.resetCounter = (TICK_RESET_GAS + self.resetCounter) if Encoder.getButtonValue() else 0

    def resetFuelData(self):
        self.checkButton()
        if self.resetCounter >= WAIT_RESET_GAS:
            self.resetCounter = 0
            self.litersConsumed = 0
            self.km100Traveled = 0.000000000001
            FileHandler.saveData(self.litersConsumed, self.km100Traveled)

    def print(self):
        self.resetFuelData()
        return 'Fuel: ' + str(self.instMpg) + ' ' + str(self.mpg)
