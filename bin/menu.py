
class Menu:
    def __init__(self, ecu1, ecu2=None):
        if ecu2 is None:
            self.ecuList = [ecu1]
        else:
            self.ecuList = [ecu1, ecu2]

    def print(self):
        printList = []
        for printing in self.ecuList:
            printList.append(printing.print())
        return printList
