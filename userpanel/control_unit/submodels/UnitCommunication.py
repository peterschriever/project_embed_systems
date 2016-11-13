from control_unit.submodels.UnitCommand import *

class UnitCommunication():

    def __init__(self):
        pass

    def sendCommand(unitCmd, controlUnits):
        # if not a list, simply make a list with one item
        if not isinstance(controlUnits, list):
            controlUnits = [controlUnits]

        results = {}
        for unit in controlUnits:
            results[unit.port] = unit.sendCommand(unitCmd)

        return results
