from ECU_commands.ecu import ECU
from constants import ESTEQUIOMETRICA, DENSIDAD_G, THROTTLE_MINIMUM, WAIT_RESET_GAS, MINIMUM_SPEED, KM_TO_SAVE_MPG, \
    WAIT_TIME_OBD, WAIT_TIME_PRINTHUB
from fileHandler import fileHandler
from lib.RotaryLibrary.encoder import Encoder


class Gas(ECU):
    def __init__(self):
        super().__init__()
        self.mpg, self.mpgSamples = fileHandler.loadData()
        self.instMPG = 0
        self.commands = {}
        self.stopped = False
        self.savedFile = False
        self.fuelMPGReset = 0
        self.km = 0
        self.auxMPG = 0
        self.auxSample = 0

    def update(self, commands):
        allCommands = commands.getCommands()
        self.commands["speed"] = allCommands["speed"]
        self.commands["throttle"] = allCommands["throttle"]
        self.commands["maf"] = allCommands["maf"]
        if self.commands["speed"] < MINIMUM_SPEED and not self.stopped:
            self.stopped = True
            fileHandler.saveData(self.mpg, self.mpgSamples)
        elif self.commands["speed"] > MINIMUM_SPEED and self.stopped:
            self.stopped = False
        self.calculateGas()

    def calculateGas(self):
        LPerS = float(self.commands["maf"]) / (
                    ESTEQUIOMETRICA * DENSIDAD_G)  # Pasamos a de g/s de aire a L/s de gasolina
        self.km += round((self.commands["speed"] / 3600 * WAIT_TIME_OBD), 2)
        if not self.stopped:  # Si voy a velocidad mayor que parada, cuenta consumo.
            if self.commands["throttle"] > THROTTLE_MINIMUM:  # Estoy acelerando?
                self.instMPG = round(LPerS * (360000 / self.commands["speed"]), 1)  # Calculamos L/100km en base a velocidad y L/s
            else:
                self.instMPG = 0.0
            self.auxMPG = ((self.auxMPG * self.auxSample + self.instMPG) / (self.auxSample + 1))
            self.auxSample += 1
            if self.km >= KM_TO_SAVE_MPG:
                self.mpg = ((self.mpg * self.mpgSamples + self.auxMPG) / (
                            self.mpgSamples + 1))  # Realizamos la media de consumo.
                self.mpgSamples += 1
                self.km = 0
                self.auxMPG = 0
                self.auxSample = 0
        else:  # Si voy a velocidad menor que parada, consumo infinito.
            self.instMPG = '---'

    def resetFuelData(self):
        if Encoder.getButtonValue():
            self.fuelMPGReset += WAIT_TIME_PRINTHUB
        if self.fuelMPGReset == WAIT_RESET_GAS:
            self.fuelMPGReset = 0
            self.mpg = 0
            self.mpgSamples = 0
            fileHandler.saveData(self.mpg, self.mpgSamples)

    def print(self):
        self.resetFuelData()
        return 'Fuel: ' + str(self.instMPG) + ' ' + str(round(self.mpg, 1))
