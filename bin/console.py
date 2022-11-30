from printhub import PrintHub

class Console(PrintHub):
    def __init__(self):
        pass

    def print(self, text):
        for i in text:
            print(i)
        print("\n")
