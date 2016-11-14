from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpRequest
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from control_unit.submodels.CommandIdentifier import *
from control_unit.submodels.UnitCommunication import *
from control_unit.submodels.UnitScanner import *

cacheDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\control_unit\\json_cache\\"

#ajax/json response generator
def buildResponse(dictIn, error=False):
    resp = {} #response dict
    if('error' in dictIn or error == True):#error array
        #2nd parameter in .get is the default value
        resp['error'] = dictIn.get('error', True)
        resp['errorcode'] = dictIn.get('errorcode', '000000')
        resp['error_msg'] = dictIn.get('error_msg', 'Unknown error')
        resp['extra'] = dictIn.get('extra', None)
    else:
        resp = dictIn
        resp['error'] = False
    return HttpResponse(json.dumps(resp))

def buildErrorResponse(dict):
    return buildResponse(dict, True)

# Create your views here.
@csrf_exempt # for debugging
def templateFunction(request):
    if request.method == "POST":
        jsonObj = json.loads(request.body.decode('utf-8'))
    else:
        jsonObj = {}
    return buildResponse(jsonObj)

@csrf_exempt # for debugging
def testCommandCommunication(request):
    getTempCmd = CommandIdentifier.getCommand('getLightLevel')
    toUnits = UnitScanner.getAllUnits()
    resolveCmd = UnitCommunication.sendCommand(getTempCmd, toUnits)
    return HttpResponse([resolveCmd])

def getConnectedDevices(request):
    tempdict = getConnectedDevicesInfo()
    d = {
        'count': len(tempdict),
        'info': tempdict
    }
    return buildResponse(d)

def getDeviceSettings(request):
    #get settings from cache
    dict = readFromCache(cacheDir + 'deviceSettings.json', 'dict')
    deviceID = request.POST.get('deviceID')
    if(deviceID == None):
        return buildResponse(dict)
    else:
        for deviceSerial in dict:
            if(deviceSerial == deviceID):
                return buildResponse(dict[deviceSerial]['settings'])
        #not found
        return buildErrorResponse({'error_msg':'Device "' + deviceID + '" not found.', \
                                  'extra':dict})

def setDeviceSettings(request):
    scanPorts() #this will force any uninitialized devices to initialize

    #get min/max and default settings from file
    #any setting not included in the POST will use the default setting
    minmaxSet = readFromCache(cacheDir + 'settingsInfo.json', 'dict')
    MINSET = minmaxSet['min']
    MAXSET = minmaxSet['max']
    default = minmaxSet['default']

    deviceID = request.POST.get('deviceID')
    newsettings['temp'] = request.POST.get('temp', default['temp'])
    newsettings['distMax'] = request.POST.get('distMax', default['distMax'])
    newsettings['distMin'] = request.POST.get('distMin', default['distMin'])
    newsettings['light'] = request.POST.get('light', default['light'])

    #check all new settings
    for setting in newsettings:
        if((newsettings[setting] > MAXSET[setting]) or (newsettings[setting] < MINSET[setting])):
            #invalid setting, throw error
            return buildErrorResponse({'error_msg':'Setting "' + setting + '" must be between "' + MINSET[setting] + '" and "' + MAXSET[setting] + '".', \
                                      'extra':{'newsettings':newsettings, 'minmaxSet':minmaxSet}})

    #all good

    #only chance the default values
    if(deviceID == 'default'):
        minmaxSet['default'] = newsettings
        writeToCache(cacheDir + 'settingsInfo.json', minmaxSet)
        return


    #get current settings from cache
    dict = readFromCache(cacheDir + 'deviceSettings.json', 'dict')


    #change ALL devices' settings, if deviceID == None (NULL);
    #otherwise only change 1 device's setting
    counter = 0
    for device in dict:
        if((deviceID == None) or (deviceID == device)):
            #save settings to device:
            if(sendCommandToDevice(dict[device]['port'], 'setSettings', newsettings)):
                counter += 1
                #update the cached dictionary
                dict[device] = {'port':dict[device]['port'], 'settings':newsettings}
            else:
                #something went wrong
                return buildErrorResponse({'error_msg':'something went wrong while trying to send new settings to the device..', \
                                          'extra':{'msg':'applied settings to ' + counter + ' devices', 'counter':counter}})
    writeToCache(cacheDir + 'deviceSettings.json', dict)

    #all done now
    return buildResponse({'msg':'applied settings to ' + counter + ' devices', 'counter':counter})

def getGraphUpdate(request):
    scanPorts() #to force update on connected device cache
    deviceID = request.POST.get('deviceID')
    sensordata = readFromCache(cacheDir + 'sensordata.json', 'dict')

    if(deviceID == None):
        #TODO
        #get data for all devices
        return
    else:
        #TODO: get current timestamp
        currentTime = 300
        timestamp = sensordata[deviceID].get('timestamp', None)
        if(timestamp == None or (currentTime - timestamp) > 3600):
            #TODO
            #get sensor data
            return buildErrorResponse({'error_msg':'this function is not yet fully supported by the API'})
        else:
            return buildResponse(sensordata[deviceID])

    return buildErrorResponse({'error_msg':'this function is not yet fully supported by the API'})

def getWindowblindState(request):

    return buildErrorResponse({'error_msg':'this function is not yet fully supported by the API'})

def setWindowblindState(request):
    return buildErrorResponse({'error_msg':'this function is not yet fully supported by the API'})
