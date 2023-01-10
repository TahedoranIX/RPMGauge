from threading import Thread
from typing import List
import time as t
import obd.obd
from Observers.observable import Observable
from Observers.observer import Observer
from constants import PORT, WAIT_TIME_OBD
from Interfaces.lcdsingle import LCDSingle
from lib import obd


class OBDSingle(Observable, object):
    observers: List[Observer] = []
    printer = None
    obd = None
    commands = {}
    exit = False

    @classmethod
    def __init__(cls, printhub=LCDSingle) -> None:
        # obd.logger.setLevel(obd.logging.DEBUG)
        cls.printer = printhub
        cls.obd = cls.connection()
        cls.commands = {"dtc": cls.obd.query(obd.commands.GET_DTC).value}
        cls.exit = False
        thread = Thread(target=cls.tick)
        thread.start()

    @classmethod
    def __del__(cls):
        try:
            cls.obd.close()
        except:
            pass

    @classmethod
    def connection(cls):
        try:
            connection = obd.OBD(PORT)
            while not connection.is_connected():
                cls.printer.print("Not connected")
                t.sleep(1)
                cls.printer.print("Connecting...")
                connection = obd.OBD(PORT, fast=False, timeout=30)
            return connection
        except:
            cls.printer.print("Problems OBD")
            t.sleep(2)
            return cls.connection()

    @classmethod
    def getCommands(cls):
        return cls.commands

    @classmethod
    def attach(cls, observer: Observer) -> None:
        cls.observers.append(observer)

    @classmethod
    def detach(cls, observer: Observer) -> None:
        cls.observers.remove(observer)

    @classmethod
    def notify(cls) -> None:
        for observer in cls.observers:
            observer.update(OBDSingle)

    @classmethod
    def getParams(cls):
        try:
            cls.commands["speed"] = int(cls.obd.query(obd.commands.SPEED).value.magnitude)
            cls.commands["rpm"] = str(cls.obd.query(obd.commands.RPM).value.magnitude)
            cls.commands["coolant"] = str(cls.obd.query(obd.commands.COOLANT_TEMP).value.magnitude)
            cls.commands["throttle"] = int(cls.obd.query(obd.commands.THROTTLE_POS).value.magnitude)
            cls.commands["maf"] = str(cls.obd.query(obd.commands.MAF).value.magnitude)
        except Exception as e:
            cls.commands["speed"] = 0
            cls.commands["rpm"] = 0
            cls.commands["coolant"] = 0
            cls.commands["throttle"] = 0
            cls.commands["maf"] = 0
            cls.notify()
            cls.obd = cls.connection()

    @classmethod
    def clearCodes(cls):
        try:
            cls.obd.query(obd.commands.CLEAR_DTC)
            cls.commands["dtc"] = cls.obd.query(obd.commands.GET_DTC).value
            if len(cls.commands["dtc"]):
                raise Exception('Cleaning error')

        except Exception as e:
            cls.printer.print("Cleaning error")


    @classmethod
    def tick(cls):
        while not cls.exit:
            cls.getParams()
            cls.notify()
            t.sleep(WAIT_TIME_OBD)

    @classmethod
    def destroy(cls):
        cls.exit = True