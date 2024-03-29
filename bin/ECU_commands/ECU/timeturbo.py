import time as t
from ECU_commands.ecu import ECU
from Interfaces.obdhandler import OBDHandler
from constants import WAIT_TURBOTIME, MINIMUM_SPEED


class TimeTurbo(ECU):
    def __init__(self):
        self.finalTime = 0
        self.stopped = False
        if 'SPEED' in OBDHandler.commands:
            OBDHandler.attach(self)

    def update(self, commands):
        speed = int(commands['SPEED'])
        if speed < MINIMUM_SPEED and not self.stopped:
            self.stopped = True
            self.finalTime = t.time() + WAIT_TURBOTIME
        elif speed > MINIMUM_SPEED and self.stopped:
            self.stopped = False

    def print(self):
        if self.stopped:
            time = self.finalTime - t.time()
            if time <= 0:
                return "Engine OFF"
            else:
                m, s = divmod(int(time), 60)
                return "Time: " + str('{:02d}:{:02d}'.format(m, s))
        else:
            return "Running"
