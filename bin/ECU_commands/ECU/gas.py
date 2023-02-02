from ECU_commands.ecu import ECU
from constants import GASOLINE_STOICHIOMETRIC, GASOLINE_DENSITY, THROTTLE_MINIMUM, WAIT_RESET_GAS, MINIMUM_SPEED, KM_TO_SAVE_MPG, \
    WAIT_REFRESH_OBD, TICK_RESET_GAS
from fileHandler import fileHandler
from lib.RotaryLibrary.encoder import Encoder


class Gas(ECU):
    def __init__(self):
        super().__init__()
        self.mpg, self.mpgSamples = fileHandler.loadData()
        self.instMpg = 0
        self.commands = {}
        self.stopped = False
        self.savedFile = False
        self.resetCounter = 0
        self.kmTraveled = 0
        self.unsavedMpg = 0
        self.unsavedSamples = 0

    def update(self, commands):
        self.commands["speed"] = commands["speed"]
        self.commands["throttle"] = commands["throttle"]
        self.commands["maf"] = commands["maf"]
        if self.commands["speed"] <= MINIMUM_SPEED and not self.stopped:
            self.stopped = True
            fileHandler.saveData(self.mpg, self.mpgSamples)
        elif self.commands["speed"] > MINIMUM_SPEED and self.stopped:
            self.stopped = False
        self.calculateGas()

    def calculateGas(self):
        literPerSeconds = self.commands["maf"] / (
                GASOLINE_STOICHIOMETRIC * GASOLINE_DENSITY)  # g/s of air to L/s of gas.
        self.kmTraveled += round((self.commands["speed"] / 3600.0 * WAIT_REFRESH_OBD), 2)
        if not self.stopped:
            if self.commands["throttle"] > THROTTLE_MINIMUM:
                self.instMpg = round(literPerSeconds * 360000.0 / self.commands["speed"], 1)  # From L/s to L/100km
            else:
                self.instMpg = 0.0
            self.unsavedMpg = ((self.unsavedMpg * self.unsavedSamples + self.instMpg) / (self.unsavedSamples + 1))
            self.unsavedSamples += 1
            if self.kmTraveled >= KM_TO_SAVE_MPG:
                self.mpg = ((self.mpg * self.mpgSamples + self.unsavedMpg) / (
                            self.mpgSamples + 1))
                self.mpgSamples += 1
                self.kmTraveled = 0
                self.unsavedMpg = 0
                self.unsavedSamples = 0
        else: # If stopped, infinite consumption
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
            self.mpg = 0
            self.mpgSamples = 0
            fileHandler.saveData(self.mpg, self.mpgSamples)

    def print(self):
        self.resetFuelData()
        return 'Fuel: ' + str(self.instMpg) + ' ' + str(round(self.mpg, 1))
