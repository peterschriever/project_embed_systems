from enum import Enum

class UnitCommand():

    def __init__(self, title, byteCode, tag):
        self.title = title
        self.tag = tag
        self.byteCode = int(byteCode, 0)

    def __str__(self):
        return "UnitCommand object: " + self.tag + ", " + self.title + ", " +\
            self.byteCode
