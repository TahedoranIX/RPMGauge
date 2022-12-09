import time as t
from ECU_commands.ecu import ECU
from constants import WAIT_TURBOTIME, MINIMUM_SPEED


class TimeTurbo(ECU):
    def __init__(self):
        super().__init__()
        self.finalTime = 0
        self.stopped = False

    def update(self, commands):
        allCommands = commands.getCommands()
        if allCommands["speed"] < MINIMUM_SPEED and not self.stopped:
            self.stopped = True
            self.finalTime = t.time() + WAIT_TURBOTIME
        elif allCommands["speed"] > MINIMUM_SPEED and self.stopped:
            self.stopped = False

    def print(self):
        if self.stopped:
            time = self.finalTime - t.time()
            if time <= 0:
                return "Engine OFF"
            else:
                return "Time: 00:" + str('{:0>2}'.format(int(time)))
        else:
            return "En marcha"
