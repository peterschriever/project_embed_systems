from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import math
import os
import sys
import time
from control_unit.functions import *
from control_unit.submodels.CommandIdentifier import *
from control_unit.submodels.UnitCommunication import *
from control_unit.submodels.UnitScanner import *

_DS = os.sep
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
cacheDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + _DS+"control_unit"+_DS+"json_cache"+_DS
configDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + _DS+"control_unit"+_DS+"config"+_DS


# ajax/json response generator
def buildResponse(dataDict, apiCommand, error = False):
    resp = {} #response dict
    if('error' in dataDict or error == True): #error array
        #2nd parameter in .get is the default value
        resp['error'] = dataDict.get('error', True)
        resp['errorcode'] = dataDict.get('errorcode', '000000')
        resp['error_msg'] = dataDict.get('error_msg', 'Unknown error')
        resp['extra'] = dataDict.get('extra', None)
    else:
        resp['command'] = apiCommand
        resp['error'] = False
        resp['data'] = dataDict
    return HttpResponse(json.dumps(resp))

def buildErrorResponse(dataDict, apiCommand):
    return buildResponse(dataDict, apiCommand, True)

def jsonPostToDict(requestBody):
    return dict(json.loads(requestBody.decode('utf-8')))

# route: /api/v1/test
# Example function
@csrf_exempt
def templateFunction(request):
    if request.META['CONTENT_TYPE'] != 'application/json':
        print("request.META['CONTENT_TYPE']", request.META['CONTENT_TYPE'])
        return buildErrorResponse({}, "test")
    postDict = jsonPostToDict(request.body)
    print("postDict", postDict)
    for key, val in postDict.items():
        print(key + ":" + val)
    return buildResponse(postDict, "test")

@csrf_exempt
def getConnectedDevices(request):
    devices = UnitScanner.getConnectedDevicesInfo()
    d = {
    'count': len(devices),
    'info': devices
    }
    return buildResponse(d, "get-connected-devices")

@csrf_exempt
def getDeviceSettings(request):
    if settings._USE_CACHE:
        devSettings = readFromCache(cacheDir + 'deviceSettings.json', 'dict')
    else:
        units = UnitScanner.getAllUnits()
        if len(units) <= 0: # no units found, error
            return buildErrorResponse({}, "get-device-settings")

        # retrieve live settings commands
        maxDistCmd = CommandIdentifier.getCommand("getMaxRollDown")
        minDistCmd = CommandIdentifier.getCommand("getMinRollDown")
        lightLimitCmd = CommandIdentifier.getCommand("getLightLimit")
        tempLimitCmd = CommandIdentifier.getCommand("getTemperatureLimit")

        cmds = [maxDistCmd, minDistCmd, lightLimitCmd, tempLimitCmd]
        unitResponses = UnitCommunication.sendGetCommand(cmds, units)

        devSettings = {} # start building devSettings dict
        for unit in units:
            if unitResponses[unit.serial] == {}: # cannot be empty
                return buildErrorResponse({}, "get-device-settings")
            devSettings[unit.serial] = {
                # NOTE: staticly typing the UnitCommand.tag out, because have
                # to change the javascript api, or make the code harder..
                "distMax": unitResponses[unit.serial]["getMaxRollDown"],
                "distMin": unitResponses[unit.serial]["getMinRollDown"],
                "light": unitResponses[unit.serial]["getLightLimit"],
                "temp": unitResponses[unit.serial]["getTemperatureLimit"],
            }

    postDict = jsonPostToDict(request.body)
    deviceID = postDict.get('deviceID')
    print("deviceID", deviceID)
    if(deviceID == None):
        return buildResponse(devSettings, "get-device-settings")
    else:
        for deviceSerial in devSettings:
            if(deviceSerial == deviceID):
                return buildResponse(devSettings[deviceSerial], "get-device-settings")
        #not found
        return buildErrorResponse({'error_msg':'Device "' + deviceID + '" not found.', \
                                  'extra':devSettings}, "get-device-settings")

@csrf_exempt
def setDeviceSettings(request):
    if settings._USE_CACHE:
        return buildErrorResponse({'error_msg':'Cache version of this cmd not implemented'}, \
                                  "set-device-settings")

    postDict = jsonPostToDict(request.body)
    deviceID = postDict.get('deviceID')
    if deviceID == None:
        return buildErrorResponse({'error_msg':'Must supply a deviceID'}, "set-device-settings")

    unit = UnitScanner.getUnitBySerial(deviceID)
    if unit == 0:
        return buildErrorResponse({'error_msg':'Device not found'}, "set-device-settings")

    setMinDistCmd = CommandIdentifier.getCommand("setMinRollDown")
    setMaxDistCmd = CommandIdentifier.getCommand("setMaxRollDown")
    setLightLimitCmd = CommandIdentifier.getCommand("setLightLimit")
    setTempLimitCmd = CommandIdentifier.getCommand("setTemperatureLimit")

    cmds = [setMaxDistCmd, setMinDistCmd, setLightLimitCmd, setTempLimitCmd]
    cmdsData = {
        "setMinRollDown": postDict.get('minRolloutAmount'),
        "setMaxRollDown": postDict.get('maxRolloutAmount'),
        "setLightLimit": postDict.get('maxLightIntensity'),
        "setTemperatureLimit": tempCToSensor(postDict.get('maxTemperature')),
    }
    unitResponses = UnitCommunication.sendSetCommand(cmds, unit, cmdsData)

    return buildResponse(unitResponses, "set-device-settings")

@csrf_exempt
def getGraphUpdate(request):
    units = UnitScanner.getAllUnits()

    getLightCmd = CommandIdentifier.getCommand('getLightLevel')
    getTempCmd = CommandIdentifier.getCommand('getTemperature')
    unitResponses = UnitCommunication.sendGetCommand([getLightCmd, getTempCmd], units)

    # dont forget to adjust the temperature
    try:
        for unit in unitResponses:
            unitResponses[unit]['getTemperature'] = tempSensorToC(unitResponses[unit]['getTemperature'])
    except Exception as e:
        return buildErrorResponse({'error_msg':'Device returned no data. \nYour device might still be loading, please try again.'}, "get-graph-update")

    return buildResponse(unitResponses, "get-graph-update")

@csrf_exempt
def getWindowblindState(request):
    postDict = jsonPostToDict(request.body)
    deviceID = postDict.get('deviceID')
    getStateCmd = CommandIdentifier.getCommand('getCurrentState')
    if deviceID == None:
        units = UnitScanner.getAllUnits()
    else:
        units = [UnitScanner.getUnitBySerial(deviceID)]

    unitResponses = UnitCommunication.sendGetCommand(getStateCmd, units)

    return buildResponse(unitResponses, "get-windowblind-state")

@csrf_exempt
def setWindowblindState(request):
    postDict = jsonPostToDict(request.body)
    deviceID = postDict.get('deviceID')
    if deviceID == None:
        return buildErrorResponse({'error_msg':'DeviceID is required'}, "set-windowblind-state")

    if postDict.get('setState') == 'up':
        setStateCmd = CommandIdentifier.getCommand('setStateRollUp')
    elif postDict.get('setState') == 'down':
        setStateCmd = CommandIdentifier.getCommand('setStateRollDown')
    else:
        return buildErrorResponse({'error_msg':'setState is required and should be either `up` or `down`'}, "set-windowblind-state")

    unit = UnitScanner.getUnitBySerial(deviceID)
    unitResponse = UnitCommunication.sendSetCommand(setStateCmd, unit, {})

    return buildResponse(unitResponse, "set-windowblind-state")

@csrf_exempt
def setWindowBlindMode(request):
    postDict = jsonPostToDict(request.body)
    deviceID = postDict.get('deviceID')
    if deviceID == None:
        return buildErrorResponse({'error_msg':'DeviceID is required'}, "set-windowblind-mode")

    if postDict.get('setMode') == 'temperature':
        setModeCmd = CommandIdentifier.getCommand('setModeTemperature')
    elif postDict.get('setMode') == 'light':
        setModeCmd = CommandIdentifier.getCommand('setModeLight')
    else:
        return buildErrorResponse({'error_msg':'setMode is required and should be either `temperature` or `light`'}, "set-windowblind-mode")

    unit = UnitScanner.getUnitBySerial(deviceID)
    unitResponse = UnitCommunication.sendSetCommand(setModeCmd, unit, {})

    return buildResponse(unitResponse, "set-windowblind-mode")
