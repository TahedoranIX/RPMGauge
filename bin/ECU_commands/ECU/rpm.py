from abc import ABC, abstractmethod

from ECU_commands.ecu import ECU
from Observers.observable import Observable
from constants import MAXIMUM_RPM, MINIMUM_RPM


class RPM(ECU, ABC):
    @abstractmethod
    def __init__(self):
        super().__init__()
        self.rpm = 0

    @abstractmethod
    def print(self):
        pass

    def update(self, commands: Observable):
        self.rpm = commands["rpm"]


class RPMNumber(RPM):
    def __init__(self):
        super().__init__()

    def print(self):
        return 'RPM: ' + str(self.rpm)


class RPMGraph(RPM):
    def __init__(self):
        super().__init__()
        self.rpmSegments = int((MAXIMUM_RPM - MINIMUM_RPM) / 16)

    def print(self):
        segments = int((float(self.rpm) - MINIMUM_RPM) / self.rpmSegments)
        segmentString = ""
        while segments > 0:
            segmentString = segmentString + 'ÿ'
            segments = segments - 1
        return segmentString
