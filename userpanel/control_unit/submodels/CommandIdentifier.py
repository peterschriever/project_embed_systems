import json
import os.path
from django.conf import settings
from control_unit.submodels.UnitCommand import *


class CommandIdentifier:
    commandsConfig = settings.BASE_DIR+'/control_unit/config/unitCommandsConfig.json'

    def __init__(self):
        pass

    def searchConfigForCmd(commandTag, unitCommandsConfig):
        for cmd in unitCommandsConfig:
            if cmd['tag'] == commandTag:
                return {
                    "byteCode": cmd['byteCode'],
                    "tag": cmd['tag'],
                    "title": cmd['title'],
                }

    def getCommand(commandTag):
        unitCommandsConfig = CommandIdentifier.loadJson()
        cmdConfig = CommandIdentifier.searchConfigForCmd(commandTag,\
            unitCommandsConfig)
        return UnitCommand(title=cmdConfig['title'],\
            byteCode=cmdConfig['byteCode'], tag=cmdConfig['tag'])

    def loadJson():
        with open(CommandIdentifier.commandsConfig, 'r') as f:
            config = json.load(f)
        return config
