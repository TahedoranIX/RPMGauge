from os import path


class FileHandler(object):
    file = str(path.realpath(path.dirname(__file__)) + "/mpg.dat")
    @classmethod
    def saveData(cls, mpg, muestras, tank=0):
        f = open(FileHandler.file, 'w')
        f.write(str(mpg))
        f.write('\n')
        f.write(str(muestras))
        f.write('\n')
        f.write(str(tank))
        f.close()

    @classmethod
    def loadData(cls):
        try:
            if path.exists(FileHandler.file):
                f = open(FileHandler.file, 'r')
                mpg = float(f.readline())
                muestras = float(f.readline())
                tank = float(f.readline())
            else:
                f = open(FileHandler.file, 'x')
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
