from control_unit.submodels.UnitCommand import *

class UnitCommunication():

    def __init__(self):
        pass

    def sendGetCommand(unitCmds, controlUnits):
        # if controlUnits is not a list, simply make a list with one item
        if not isinstance(controlUnits, list):
            controlUnits = [controlUnits]

        # if unitCmds is not a list, simply make a list with one item
        if not isinstance(unitCmds, list):
            unitCmds = [unitCmds]

        results = {}
        for unit in controlUnits:
            results[unit.serial] = unit.sendGetCommand(unitCmds)

        return results # is a dictionary: {unit.serial: responseCode}

    def sendSetCommand(unitCmds, controlUnits, cmdsData):
        # if controlUnits is not a list, simply make a list with one item
        if not isinstance(controlUnits, list):
            controlUnits = [controlUnits]

        # if unitCmds is not a list, simply make a list with one item
        if not isinstance(unitCmds, list):
            unitCmds = [unitCmds]

        results = {}
        for unit in controlUnits:
            results[unit.serial] = unit.sendSetCommand(unitCmds, cmdsData)

        return results # is a dictionary: {unit.serial: responseCode}
