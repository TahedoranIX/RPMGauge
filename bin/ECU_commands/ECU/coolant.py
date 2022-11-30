from ECU_commands.ecu import ECU


class Coolant(ECU):
    def __init__(self):
        self.coolOBD = None

    def update(self, commands):
        self.coolOBD = commands["coolant"]

    def print(self):
        return 'Temp: ' + self.coolOBD + ' C'
