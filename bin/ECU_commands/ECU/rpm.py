from abc import ABC, abstractmethod

from ECU_commands.ecu import ECU
from Observers.observable import Observable
from constants import MAXIMUM_RPM, MINIMUM_RPM


class RPM(ECU, ABC):
    def __init__(self):
        super().__init__()
        self.rpm = 5
        self.rpmSegments = int((MAXIMUM_RPM - MINIMUM_RPM) / 16)

    @abstractmethod
    def print(self):
        pass

    def update(self, commands: Observable):
        command = commands.getCommands()
        self.rpm = command["rpm"]


class RPMNumber(RPM):
    def __init__(self):
        super().__init__()

    def print(self):
        return 'RPM: ' + str(self.rpm)

class RPMGraph(RPM):
    def __init__(self):
        super().__init__()

    def print(self):
        segment = int((float(self.rpm) - MINIMUM_RPM) / self.rpmSegments)
        segmentList = ""
        while segment > 0:
            segmentList = segmentList + 'ÿ'
            segment = segment - 1
        return segmentList
