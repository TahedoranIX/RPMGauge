from abc import ABC, abstractmethod
from ecu import ECU

MINIMUM_RPM = 1200
MAXIMUM_RPM = 5500

class RPM(ABC, ECU):
    def __init__(self):
        ECU.__init__(self)
        self.__rpmSegments = int((MAXIMUM_RPM - MINIMUM_RPM) / 16)

    def print(self):
        return 'Temp: ' + self.__command["coolant"] + ' C'


class RPMNumber(RPM):
    def __init__(self):
        RPM.__init__(self)

    def print(self):
        return 'RPM: ' + self.__command["rpm"]


class RPMGraph(RPM):
    def __init__(self):
        ECU.__init__(self)

    def print(self):
        segment = int((float(self.__command["rpm"]) - MINIMUM_RPM) / self.__rpmSegments)
        segmentList = []
        while segment > 0:
            segmentList.append(255)
            segment = segment - 1
        return segmentList
