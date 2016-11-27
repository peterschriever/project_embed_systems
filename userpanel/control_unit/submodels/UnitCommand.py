from enum import Enum

class UnitCommand():

    def __init__(self, title, byteCode, tag, sendMore):
        self.title = title
        self.tag = tag
        self.byteCode = int(byteCode, 16)
        self.sendMore = sendMore

    def __str__(self):
        return "UnitCommand object: " + self.tag + ", " + self.title + ", " +\
            str(self.byteCode)
