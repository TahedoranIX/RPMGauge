from ECU_commands.ecu import ECU, MINIMUM_SPEED

class Gas(ECU):
    def __init__(self):
        super().__init__()
        self.instMPG = None
        self.mpg = None
        self.mpgSamples = None
        self.commands = {}
        self.stopped = False

    def update(self, commands):
        allCommands = commands.getCommands()
        self.commands["speed"] = allCommands["speed"]
        self.commands["throttle"] = allCommands["throttle"]
        self.commands["maf"] = allCommands["maf"]
        if self.commands["speed"] < MINIMUM_SPEED and not self.stopped:
            self.stopped = True
        elif self.commands["speed"] > MINIMUM_SPEED and self.stopped:
            self.stopped = False
    def print(self):
        return 'Temp: ' + self.commands["speed"]