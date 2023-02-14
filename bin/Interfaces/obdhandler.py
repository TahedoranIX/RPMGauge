import logging
from threading import Thread
from typing import List
import time as t
from Observers.observable import Observable
from Observers.observer import Observer
from constants import PORT, WAIT_REFRESH_OBD, GENERAL
from obd import obd

logger = logging.getLogger(GENERAL)

class OBDHandler(Observable, object):
    observers: List[Observer] = []
    printer = None
    obd = None
    commands = {
        "SPEED": None,
        "RPM": None,
        "COOLANT_TEMP": None,
        "THROTTLE_POS": None,
        "MAF": None,
        "FUEL_RATE": None,
        "OIL_TEMP": None,
        "O2_B1S1": None
    }
    exit = False

    @classmethod
    def __init__(cls, printhub) -> None:
        cls.printer = printhub
        cls.obd = cls.connection()
        cls.initCommands()
        cls.exit = False
        thread = Thread(target=cls.tick)
        thread.start()

    @classmethod
    def initCommands(cls):
        unsupported = []
        for key in cls.commands:
            if cls.obd.supports(obd.commands[key]):
                logger.debug('Command: ' + key + ' supported.')
                cls.commands[key] = cls.obd.query(obd.commands[key]).value.magnitude
            else:
                logger.debug('Command: ' + key + ' not supported.')
                unsupported.append(key)

        for key in unsupported:
            del cls.commands[key]

        if cls.obd.supports(obd.commands.GET_DTC):
            logger.debug('Command: get_dtc supported.')
            cls.commands['GET_DTC'] = cls.obd.query(obd.commands.GET_DTC).value
        else:
            cls.commands['GET_DTC'] = []

    @classmethod
    def __del__(cls):
        try:
            cls.obd.close()
        except:
            pass

    @classmethod
    def connection(cls):
        try:
            cls.printer.print("Connecting...")
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
    def attach(cls, observer: Observer) -> None:
        cls.observers.append(observer)

    @classmethod
    def detach(cls, observer: Observer) -> None:
        cls.observers.remove(observer)

    @classmethod
    def notify(cls) -> None:
        for observer in cls.observers:
            observer.update(OBDHandler.commands)

    @classmethod
    def getParams(cls):
        try:
            logger.debug('Registering params from OBD.')
            for key in cls.commands:
                if key != 'GET_DTC':
                    cls.commands[key] = cls.obd.query(obd.commands[key]).value.magnitude

        except Exception as e:
            logger.error('Error while getting params from OBD.')
            for key in cls.commands:
                if key != 'GET_DTC':
                    cls.commands[key] = 0
            cls.notify()
            logger.error('Resetting connection.')
            cls.obd = cls.connection()

    @classmethod
    def clearCodes(cls):
        try:
            logger.debug('Clearing dtc in OBD.')
            cls.obd.query(obd.commands.CLEAR_DTC)
            cls.commands["GET_DTC"] = cls.obd.query(obd.commands.GET_DTC).value
            if len(cls.commands["GET_DTC"]):
                raise Exception()

        except Exception as e:
            logger.error('Error cleaning dtc in OBD.')
            cls.printer.print("Cleaning error")


    @classmethod
    def tick(cls):
        while not cls.exit:
            cls.getParams()
            cls.notify()
            t.sleep(WAIT_REFRESH_OBD)

    @classmethod
    def destroy(cls):
        cls.exit = True
