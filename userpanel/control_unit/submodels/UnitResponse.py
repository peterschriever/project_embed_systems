from enum import Enum

class UnitResponse():

    def __init__(self, title, byteCode, response, collectMore):
        self.title = title
        self.response = response
        self.collectMore = collectMore
        self.byteCode = int(byteCode, 16)

    def __str__(self):
        return "UnitResponse object: " + self.response + ", " + self.title + ", " +\
            str(self.byteCode) + ", " + str(self.collectMore)
