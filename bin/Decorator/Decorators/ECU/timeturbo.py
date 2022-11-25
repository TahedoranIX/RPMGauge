# from Decorator.component import Component
import time as t

from Decorator.Decorators.ECU.ecu import ECU

MAX_TIME = 60


class TimeTurbo(ECU):
    def __init__(self):
        super(ECU).__init__()
        self.__finalTime = 0
        self.__actualTime = 0

    def update(self, commands):
        ECU.__commands = commands
        if commands["speed"] < ECU.MINIMUM_SPEED and not self._stopped:
            self.__stopped = True
            self.__finalTime = t.time() + MAX_TIME
        elif commands["speed"] > ECU.MINIMUM_SPEED and self.__stopped:
            self.__stopped = False

    def print(self):
        if ECU.__stopped:
            time = self.__finalTime - self.__actualTime
            if time <= 0:
                return "Engine OFF"
            else:
                return "Time: 00:" + str('{:0>2}'.format(int(time)))
        else:
            return "En marcha"


if __name__ == "__main__":
    time = TimeTurbo()
    time.update({"speed": 4})
    print(time.print())
