
class Menu:
    def __init__(self, ecu1, ecu2=None):
        self.ecuList = [ecu1, ecu2]

    def print(self):
        if self.ecuList[1] is None:
            return self.ecuList[0].print()
        else:
            return [self.ecuList[0].print(), self.ecuList[1].print()]

