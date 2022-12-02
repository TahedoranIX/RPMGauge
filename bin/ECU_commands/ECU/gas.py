from abc import ABC, abstractmethod
from ECU_commands.ecu import ECU
from constants import ESTEQUIOMETRICA, DENSIDAD_G, THROTTLE_MINIMUM, WAIT_RESET_GAS, MINIMUM_SPEED
from fileHandler import fileHandler
from lib.RotaryLibrary.encoder import Encoder


class Gas(ECU, ABC):
    def __init__(self):
        super().__init__()
        self.mpg, self.mpgSamples = fileHandler.loadData()
        self.instMPG = 0
        self.commands = {}
        self.stopped = False
        self.savedFile = False
        self.fuelMPGReset = 0
    @abstractmethod
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

    """
    Calculate the 
    """
    def calculateGas(self):
        LPerS = float(self.commands["maf"]) / (ESTEQUIOMETRICA * DENSIDAD_G)  # Pasamos a de g/s de aire a L/s de gasolina

        # if self.__fuelTank > 0:  # Si hay litros en el tanque (más estilistico)
        #     self.__fuelTank -= self.__LPerS * 2  # Restamos la cantidad de combustible que queda.

        if not self.stopped:  # Si voy a velocidad mayor que parada, cuenta consumo.
            if self.commands["throttle"] > THROTTLE_MINIMUM:  # Estoy acelerando?
                self.instMPG = round(LPerS * (360000 / (self.commands["speed"] + 0.0000001)), 1)  # Calculamos L/100km en base a velocidad y L/s
            else:
                self.instMPG = 0.0
            self.mpg = ((self.mpg * self.mpgSamples + self.instMPG) / (self.mpgSamples + 1))  # Realizamos la media de consumo.
            self.mpgSamples += 1
        else:  # Si voy a velocidad menor que parada, consumo infinito.
            self.instMPG = '---'

    def resetFuelData(self):
        if Encoder.getButtonValue():
            self.fuelMPGReset += 1
        if self.fuelMPGReset == WAIT_RESET_GAS:  # Si el boton del rotatory esta pulsado durante 6*0.5s, se reinician los datos de consumos.
            self.fuelMPGReset = 0
            self.mpg = 0
            self.mpgSamples = 0
            fileHandler.saveData(self.mpg, self.mpgSamples)

    @abstractmethod
    def print(self):
        self.resetFuelData()
        return 'Fuel: ' + str(self.instMPG) + ' ' + str(round(self.mpg, 1))
