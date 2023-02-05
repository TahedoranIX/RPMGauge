from ECU_commands.ecu import ECU
from Interfaces.obdhandler import OBDHandler
from car import Car
from constants import THROTTLE_MINIMUM, WAIT_RESET_GAS, MINIMUM_SPEED, KM_TO_SAVE_MPG, \
    WAIT_REFRESH_OBD, TICK_RESET_GAS
from fileHandler import fileHandler
from lib.RotaryLibrary.encoder import Encoder

class Gas(ECU):
    def __init__(self):
        super().__init__()
        self.litersConsumed, self.kmTraveled = fileHandler.loadData()
        self.mpg = round(self.litersConsumed * 100.0 / (self.kmTraveled + 0.0000000001), 1)
        self.kmToSave = 0
        self.instMpg = 0
        self.commands = {}
        self.stopped = False
        self.savedFile = False
        self.resetCounter = 0
        if 'MAF' and 'THROTTLE_POS' and 'SPEED' in OBDHandler.commands:
            OBDHandler.attach(self)

    def update(self, commands):
        self.commands["speed"] = commands["SPEED"]
        self.commands["throttle"] = commands["THROTTLE_POS"]
        self.commands["maf"] = commands["MAF"]
        if self.commands["speed"] <= MINIMUM_SPEED and not self.stopped:
            self.stopped = True
            fileHandler.saveData(self.litersConsumed, self.kmTraveled)
        elif self.commands["speed"] > MINIMUM_SPEED and self.stopped:
            self.stopped = False
        self.calculateGas()

    def mafConversion(self):
        return float((self.commands["maf"] / (
                Car.stoichiometric * Car.density)))  # g/s of air to L/s of gas.

    def calculateGas(self):
        liters = self.mafConversion()
        self.litersConsumed += liters * WAIT_REFRESH_OBD
        self.kmToSave += self.commands["speed"] / 3600.0 * WAIT_REFRESH_OBD
        self.kmTraveled += self.commands["speed"] / 3600.0 * WAIT_REFRESH_OBD
        if not self.stopped:
            if self.commands["throttle"] > THROTTLE_MINIMUM:
                self.instMpg = round(liters * 360000.0 / self.commands["speed"], 1)  # From L/s to L/100km
            else:
                self.instMpg = 0.0
            if self.kmToSave >= KM_TO_SAVE_MPG:
                self.mpg = round(self.litersConsumed * 100.0 / self.kmTraveled, 1)  # L/100km
                self.kmToSave = 0

        else:  # If stopped, infinite consumption
            self.instMpg = '---'

    def checkButton(self):
        if Encoder.getButtonValue():
            self.resetCounter += TICK_RESET_GAS
        else:
            self.resetCounter = 0

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
