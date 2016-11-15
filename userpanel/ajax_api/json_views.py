from django.http import HttpResponse
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from control_unit.functions import *

cacheDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\control_unit\\json_cache\\"
configDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\control_unit\\config\\"


#ajax/json response generator
def buildResponse(dict, error=False):
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