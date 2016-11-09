from django.http import HttpResponse
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from control_unit.functions import *

cacheDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\control_unit\\json_cache\\"


# Create your views here.
def templateFunction(request):
    for key, val in request.POST.items():
        #do stuff
        print(key + ":" + val)
    return HttpResponse(json.dumps(request.POST))

def getConnectedDevices(request):
    d = {
        'count': countConnectedDevices(),
        'info': readFromCache(cacheDir + 'devices.json', 'dict')
    }
    return HttpResponse(json.dumps(d))

def getDeviceSettings(request):
    #get settings from cache
    dict = readFromCache(cacheDir + 'deviceSettings.json', 'dict')
    deviceID = request.POST.get('deviceID')
    if(deviceID == None):
        return HttpResponse(json.dumps(dict))
    else:
        for deviceSerial in dict:
            if(deviceSerial == deviceID):
                return HttpResponse(json.dumps(dict[deviceSerial]['settings']))
        #not found
        return HtppResponse(json.dumps({'errorcode':'000001', \
                            'error_msg':'Device "' + deviceID + '" not found.', \
                            'extra':dict}))
                            
def setDeviceSettings(request):
    #TODO:
    #handle devices that haven't been manually added to the json file
    
    #get min/max settings from file
    minmaxSet = readFromCache(cacheDir + 'minmaxSettings.json', 'dict')
    MINSET = minmaxSet['min']
    MAXSET = minmaxSet['max']
    
    deviceID = request.POST.get('deviceID')
    newsettings['temp'] = request.POST.get('temp')
    newsettings['distMax'] = request.POST.get('distMax')
    newsettings['distMin'] = request.POST.get('distMin')
    newsettings['light'] = request.POST.get('light')
    
    #check all new settings
    for setting in newsettings:
        if((newsettings[setting] > MAXSET[setting]) | (newsettings[setting] < MINSET[setting])):
            return HttpResponse(json.dumps({'errorcode':'000010', \
                               'error_msg':'Setting "' + setting + '" must be between "' + MINSET[setting] + '" and "' + MAXSET[setting] + '".', \
                               'extra':{'newsettings':newsettings, 'minmaxSet':minmaxSet}}))
    #all good
        
    #get current settings from cache
    dict = readFromCache(cacheDir + 'deviceSettings.json', 'dict')
    
    if(deviceID == None):
        #change ALL devices' settings, if deviceID == None (NULL);
        #otherwise only change 1 device's setting
        for device in dict:
            if((deviceID == None) | (deviceID == device)):
                dict[device] = {'port':dict[device][port], 'settings':newsettings}
    #TODO: make
    #applySettings()
    #a function in functions.py, to send the settings to all connected devices