from typing import List


class Menu:
    def __init__(self, ecuList: List):
        self.ecuList = ecuList

    def print(self):
        printList = []
        for printing in self.ecuList:
            printList.append(printing.print())
        return printList
