from ECU_commands.ecu import ECU
from Interfaces.obdhandler import OBDHandler
from car import Car
from constants import THROTTLE_MINIMUM, WAIT_RESET_GAS, MINIMUM_SPEED, KM_TO_SAVE_MPG, \
    WAIT_REFRESH_OBD, TICK_RESET_GAS
from fileHandler import fileHandler
from lib.RotaryLibrary.encoder import Encoder

class Gas(ECU):
    def __init__(self):
        self.litersConsumed, self.kmTraveled = fileHandler.loadData()
        self.mpg = round(self.litersConsumed * 100.0 / (self.kmTraveled + 0.0000000001), 1)
        self.instMpg = 0
        self.stopped = False
        self.savedFile = False
        self.resetCounter = 0
        if 'THROTTLE_POS' and 'SPEED' in OBDHandler.commands:
            if 'FUEL_RATE' in OBDHandler.commands:
                self.commands = {
                    'THROTTLE_POS': OBDHandler.commands['THROTTLE_POS'],
                    'SPEED': OBDHandler.commands['SPEED'],
                    'FUEL_RATE': OBDHandler.commands['FUEL_RATE']
                }
                self.fuelRate = True
                OBDHandler.attach(self)
            elif 'MAF' in OBDHandler.commands:
                self.commands = {
                    'THROTTLE_POS': OBDHandler.commands['THROTTLE_POS'],
                    'SPEED': OBDHandler.commands['SPEED'],
                    'MAF': OBDHandler.commands['MAF']
                }
                self.fuelRate = False
                OBDHandler.attach(self)

    def update(self, commands):
        for key in self.commands:
            self.commands[key] = commands[key]
        if self.commands["SPEED"] <= MINIMUM_SPEED and not self.stopped:
            self.stopped = True
            fileHandler.saveData(self.litersConsumed, self.kmTraveled)
        elif self.commands["SPEED"] > MINIMUM_SPEED and self.stopped:
            self.stopped = False
        self.calculateGas()

    def mafConversion(self):
        return (self.commands["MAF"] / (
                Car.stoichiometric * Car.density))  # g/s of air to L/s of gas.

    def calculateGas(self):
        if not self.stopped:
            self.kmTraveled += self.commands["SPEED"] / 3600.0 * WAIT_REFRESH_OBD
            if self.commands["THROTTLE_POS"] > THROTTLE_MINIMUM:
                literS = (self.commands["FUEL_RATE"] / 3600.0) if self.fuelRate else self.mafConversion()
                self.litersConsumed += literS * WAIT_REFRESH_OBD
                self.instMpg = round(literS * 360000.0 / self.commands["SPEED"], 1)  # From L/s to L/100km
            else:
                self.instMpg = 0.0
            self.mpg = round(self.litersConsumed * 100.0 / self.kmTraveled, 1)  # L/100km

        else:  # If stopped, infinite consumption
            self.instMpg = '---'

    def checkButton(self):
        self.resetCounter = TICK_RESET_GAS + self.resetCounter if Encoder.getButtonValue() else 0

    def resetFuelData(self):
        self.checkButton()
        if self.resetCounter >= WAIT_RESET_GAS:
            self.resetCounter = 0
            self.litersConsumed = 0
            self.kmTraveled = 0
            fileHandler.saveData(self.litersConsumed, self.kmTraveled)

    def print(self):
        self.resetFuelData()
        return 'Fuel: ' + str(self.instMpg) + ' ' + str(self.mpg)
