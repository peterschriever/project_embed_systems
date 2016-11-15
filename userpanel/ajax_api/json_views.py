from django.http import HttpResponse
import json
import math
import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from control_unit.functions import *

_DS = os.sep
cacheDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + _DS+"control_unit"+_DS+"json_cache"+_DS
configDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + _DS+"control_unit"+_DS+"config"+_DS


#ajax/json response generator
def buildResponse(dict, error = False):
    resp = {} #response dict
    if('error' in dict or error == True):#error array
        #2nd parameter in .get is the default value
        resp['error'] = dict.get('error', True)
        resp['errorcode'] = dict.get('errorcode', '000000')
        resp['error_msg'] = dict.get('error_msg', 'Unknown error')
        resp['extra'] = dict.get('extra', None)
    else:
        resp = dict
        resp['error'] = False
    return HttpResponse(json.dumps(resp))

def buildErrorResponse(dict):
    return buildResponse(dict, True)

# Create your views here.
def templateFunction(request):
    for key, val in request.POST.items():
        #do stuff
        print(key + ":" + val)
    return buildResponse(request.POST)

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
    minmaxSet = readFromCache(configDir + 'settingsConfig.json', 'dict')
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
        writeToCache(configDir + 'settingsConfig.json', minmaxSet)
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
                dict[device] = newsettings
            else:
                #something went wrong
                return buildErrorResponse({'error_msg':'something went wrong while trying to send new settings to the device..', \
                                          'extra':{'msg':'applied settings to ' + counter + ' devices', 'counter':counter}})
    writeToCache(cacheDir + 'deviceSettings.json', dict)

    #all done now
    return buildResponse({'msg':'applied settings to ' + counter + ' devices', 'counter':counter})

def getGraphUpdate(request):
    deviceports = scanPorts('ports') #to force update on connected devices cache
    deviceID = request.POST.get('deviceID')
    if(deviceID == ""):
        deviceID = None
    sensordata = readFromCache(cacheDir + 'sensordata.json', 'dict')
    currentTime = int(math.floor(time.time()))
    returndata = {}
    newSensordata = sensordata

    if(deviceports == {}):
        return buildErrorResponse({'error_msg':'aaaaaaaaaaaaaaaargh'})

    for dev, port in deviceports.items():
        if(deviceID == None or deviceID == dev):
            timestamp = sensordata.get(dev, {'timestamp':None}).get('timestamp', None)
            if(timestamp == None or (currentTime - int(timestamp)) > 3600):
                result = sendCommandToDevice(port, 'getSensorValues')
                if(result == None):
                    return buildErrorResponse({'error_msg':'failed to retrieve sensor values from device'})
                else:
                    result['temp'] = tempSensorToC(result['temp'])
                    returndata[dev] = [result['temp'], result['light']]
                    newSensordata[dev] = {'timestamp':currentTime, 'temp':result['temp'], 'light':result['light']}
                    print("newSensordata[dev]", newSensordata[dev])
            else:
                returndata[dev] = [sensordata.get(dev, 'temp'), sensordata.get(dev, 'light')]
    writeToCache(cacheDir + 'sensordata.json', newSensordata)

    return buildResponse({'data':returndata})

def getWindowblindState(request):

    return buildErrorResponse({'error_msg':'this function is not yet fully supported by the API', 'errorcode':'111111'})

def setWindowblindState(request):
    return buildErrorResponse({'error_msg':'this function is not yet fully supported by the API', 'errorcode':'111111'})
