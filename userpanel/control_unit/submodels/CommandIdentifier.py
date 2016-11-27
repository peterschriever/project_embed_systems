import json
import os.path
from django.conf import settings
from control_unit.submodels.UnitCommand import *
from control_unit.submodels.UnitResponse import *


class CommandIdentifier:
    commandsConfig = settings.BASE_DIR+'/control_unit/config/unitCommandsConfig.json'

    def __init__(self):
        pass

    def searchConfigForCmd(commandTag, unitCommandsConfig):
        for cmd in unitCommandsConfig:
            if cmd['tag'] == commandTag:
                result = {
                    "byteCode": cmd['byteCode'],
                    "tag": cmd['tag'],
                    "title": cmd['title'],
                }
                try:
                    result['sendMore'] = cmd['sendMore']
                except Exception as e:
                    result['sendMore'] = 0
                return result

    def searchConfigForResp(byteCode, unitCommandsConfig):
        for cmd in unitCommandsConfig:
            if cmd['byteCode'] == byteCode:
                return {
                    "byteCode": cmd['byteCode'],
                    "response": cmd['response'],
                    "title": cmd['title'],
                    "collectMore": cmd['collectMore'],
                }

    def getCommand(commandTag):
        unitCommandsConfig = CommandIdentifier.loadJson()
        cmdConfig = CommandIdentifier.searchConfigForCmd(commandTag,\
            unitCommandsConfig)
        return UnitCommand(title=cmdConfig['title'], sendMore=cmdConfig['sendMore'], \
            byteCode=cmdConfig['byteCode'], tag=cmdConfig['tag'])

    def getResponse(byteCode):
        unitCommandsConfig = CommandIdentifier.loadJson()
        cmdConfig = CommandIdentifier.searchConfigForResp(byteCode,\
            unitCommandsConfig)
        return UnitResponse(title=cmdConfig['title'],\
            byteCode=cmdConfig['byteCode'], response=cmdConfig['response'], \
            collectMore=cmdConfig['collectMore'])

    def loadJson():
        with open(CommandIdentifier.commandsConfig, 'r') as f:
            config = json.load(f)
        return config
