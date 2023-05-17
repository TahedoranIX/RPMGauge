import logging
from os import path

from constants import GENERAL

logger = logging.getLogger(GENERAL)

class FileHandler(object):
    file = str(path.realpath(path.dirname(__file__)) + "/resources/mpg.dat")
    @classmethod
    def saveData(cls, mpg, muestras, tank=0):
        logger.debug('Init saving data')
        f = open(cls.file, 'w')
        f.write(str(mpg))
        f.write('\n')
        f.write(str(muestras))
        f.write('\n')
        f.write(str(tank))
        f.close()
        logger.debug('Saving data successfully')

    @classmethod
    def loadData(cls):
        try:
            logger.debug('Trying to access file')
            if path.exists(cls.file):
                f = open(cls.file, 'r')
                mpg = float(f.readline())
                muestras = float(f.readline())
                tank = float(f.readline())
            else:
                logger.debug('Creating file')
                f = open(cls.file, 'x')
                f.write('0\n0\n0.000000000001')
                mpg = 0
                muestras = 0.000000000001
                tank = 0
            f.close()
            logger.debug('Data obtained successfully')
            return mpg, muestras

        except Exception as e:
            logger.error("Can't create file")
            mpg = 0
            muestras = 0.000000000001
            tank = 0
            return mpg, muestras
