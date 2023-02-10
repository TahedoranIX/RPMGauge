from os import path

class FileHandler(object):
    file = str(path.realpath(path.dirname(__file__)) + "/mpg.dat")
    @classmethod
    def saveData(cls, mpg, muestras, tank=0):
        f = open(cls.file, 'w')
        f.write(str(mpg))
        f.write('\n')
        f.write(str(muestras))
        f.write('\n')
        f.write(str(tank))
        f.close()

    @classmethod
    def loadData(cls):
        try:
            if path.exists(cls.file):
                f = open(cls.file, 'r')
                mpg = float(f.readline())
                muestras = float(f.readline())
                tank = float(f.readline())
            else:
                f = open(cls.file, 'x')
                f.write('0\n0\n0.000000000001')
                mpg = 0
                muestras = 0.000000000001
                tank = 0
            f.close()
            return mpg, muestras

        except Exception as e:
            print("cant create file")
            mpg = 0
            muestras = 0.000000000001
            tank = 0
            return mpg, muestras
