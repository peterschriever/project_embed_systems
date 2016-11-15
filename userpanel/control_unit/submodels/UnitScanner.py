import json
import os
import serial
import serial.tools.list_ports
from control_unit.submodels.ControlUnit import *

class UnitScanner:
    cacheDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/json_cache/"

    def __init__(self):
        pass

    def getAllUnits():
        UnitScanner.rescanPorts() # refresh cache?
        jsonDevices = UnitScanner.readFromCache(UnitScanner.cacheDir + 'devices.json')
        devicesData = json.loads(jsonDevices)

        controlUnits = []
        for devKey in devicesData:
            controlUnits.append(ControlUnit( port=devicesData[devKey]['port'],\
                description=devicesData[devKey]['serial'], serial="buggyOnLinux?" ))

        return controlUnits

    def rescanPorts():
        UnitScanner.writeToCache(UnitScanner.cacheDir + 'devices.json', '{}')
        ports = []
        for device in serial.tools.list_ports.comports():
            if((device.description).find("Arduino Uno") != -1):
                if(UnitScanner.isNewDevice(device)):
                    UnitScanner.initNewDevice(device)

                ports.append((device.device, device.serial_number, device.description))
        return ports

    def isNewDevice(device): #device from scanPorts()
        settingcache = UnitScanner.readFromCache(UnitScanner.cacheDir + "deviceSettings.json", 'dict')

        if(device.serial_number in settingcache):
            return False
        else:
            return True

    def initNewDevice(device): #device from scanPorts()
        settingsCache = UnitScanner.readFromCache(UnitScanner.cacheDir \
            + "deviceSettings.json", 'dict')
        deviceCache = UnitScanner.readFromCache(UnitScanner.cacheDir \
            + "devices.json", 'dict')

        if((device.serial_number in settingsCache) == False): #if not in cache
            default = UnitScanner.readFromCache(UnitScanner.cacheDir +\
                'settingsInfo.json', 'dict')
            newSettingsCache = settingsCache.get(device.serial_number, default)
            UnitScanner.writeToCache(UnitScanner.cacheDir + 'settingsInfo.json', newSettingsCache)
        i = 0
        for dev in deviceCache:
            i += 1
            if(deviceCache[dev]['serial'] == device.serial_number):
                return #all done

        #add device to deviceCache
        deviceCache[i] = {'port':device[0], \
            'serial':device[1], \
            'description':device[2]}
        UnitScanner.writeToCache(UnitScanner.cacheDir + 'devices.json', deviceCache)
        return #all done

    def readFromCache(location, returntype='string'):
        with open(location, 'r') as jsonfile:
            jsondata = json.load(jsonfile)
            if(returntype == 'string'):
                return json.dumps(jsondata)
            else: #dict
                return jsondata

    def writeToCache(location, data, deprec=''):
        with open(location, 'w') as jsonfile:
            if(isinstance(data, str)):
                jsonfile.write(str(data))
                return True
            elif(isinstance(data, dict)): #dict
                json.dump(data, jsonfile)
                return True
            else:
                #error
                return False

    def getConnectedDevicesInfo():
        deviceinfo = UnitScanner.scanPorts('all')

        parsedinfo = {}
        i = 0
        for device in deviceinfo:
            parsedinfo[i] = {'port':device[0], \
            'serial':device[1], \
            'description':device[2]}
            i += 1

        UnitScanner.writeToCache(UnitScanner.cacheDir + "devices.json", parsedinfo)

        return deviceinfo
