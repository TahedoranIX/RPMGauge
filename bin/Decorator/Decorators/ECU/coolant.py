from ecu import ECU


class Coolant(ECU):
    def __init__(self):
        ECU.__init__(self)

    def print(self):
        return 'Temp: ' + self.__command["coolant"] + ' C'
