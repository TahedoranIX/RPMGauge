from os.path import exists

from constants import FILE_HANDLER


class fileHandler(object):

    @classmethod
    def saveData(cls, mpg, muestras, tank=0):
        f = open(FILE_HANDLER, 'w')
        f.write(str(mpg))
        f.write('\n')
        f.write(str(muestras))
        f.write('\n')
        f.write(str(tank))
        f.close()

    @classmethod
    def loadData(cls):
        try:
            if exists(FILE_HANDLER):
                f = open(FILE_HANDLER, 'r')
                mpg = float(f.readline())
                muestras = float(f.readline())
                tank = float(f.readline())
            else:
                f = open(FILE_HANDLER, 'x')
                f.write('0\n0\n0')
                mpg = 0
                muestras = 0
                tank = 0
            f.close()
            return mpg, muestras

        except Exception as e:
            print("cant create file")
            mpg = 0
            muestras = 0
            tank = 0
            return mpg, muestras
