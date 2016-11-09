from control_unit.scanPorts import *
import json
import os


cacheDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\control_unit\\json_cache\\"


def readFromCache(location, returntype='string'):
    with open(location, 'r') as jsonfile:
        jsondata = json.load(jsonfile)
        if(returntype == 'string'):
            return json.dumps(jsondata)
        else: #dict
            return jsondata
    
def writeToCache(location, data, inputtype='string'): 
    with open(location, 'w') as jsonfile:
        if(inputtype == 'string'):
            jsonfile.write(str(data))
        else: #dict
            json.dump(data, jsonfile)
            
#using countConnectedDevices automatically updates the devices.json cache
def countConnectedDevices():
    deviceinfo = scanPorts('all')
    
    parsedinfo = {}
    i = 0
    for device in deviceinfo:
        print(device)
        parsedinfo[i] = {'port':device[0], \
        'serial':device[1], \
        'description':device[2]}
        i += 1
    
    writeToCache(cacheDir + "devices.json", parsedinfo, 'dict')
    
    return len(deviceinfo)
    