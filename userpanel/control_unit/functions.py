import json
import os
import serial
import serial.tools.list_ports
import time


cacheDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\control_unit\\json_cache\\"
configDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\control_unit\\config\\"

def scanPorts(info = ""):
    if(info == 'ports'):
        ports = {}
    else:
        ports = []
    for device in serial.tools.list_ports.comports():
        if((device.description).find("Arduino Uno") != -1):
            if(isNewDevice(device)):
                initNewDevice(device)
            if(info == 'all'):
                ports.append([device.device, device.serial_number, device.description])
            elif(info == 'ports'):
                ports[device.serial_number] = device.device
            else:
                ports.append(device.device)
    return ports


def readFromCache(location, returntype = 'string'):
    with open(location, 'r') as jsonfile:
        jsondata = json.load(jsonfile)
        if(returntype == 'string'):
            return json.dumps(jsondata)
        else: #dict
            return jsondata

def writeToCache(location, data):
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

def readByte(ser):
    return ord(ser.read(1));

def readDoubleByte(ser):
    return (ord(ser.read(1)) << 8) + ord(ser.read(1))

#reads @length@ from @device@; where @device@ is either port or serial
#@lenght@ will generally be either 8 or 16
def readFromDevice(device, length = 8):
    devlist = scanPorts('all')
    port = None
    for dev in devlist:
        if(dev['0'] == device or dev['1'] == device):
            port = dev['port']
            break #get out of the for loop
    if(port == None):
        #device not connected/found
        return None
    elif(isinstance(length, int) and (length > 1) and (length < 100)):
        #init serial connection
        ser = serial.Serial(port, 19200)
        return ser.read(length)
    else:
        #if not a number, or not between 1 and 100, then don't try reading
        return None

#writes @data@ to @device@; where @device@ is either port or serial
#@data@ should be of type bytes
def writeToDevice(device, data):
    devlist = scanPorts('all')
    port = None
    for dev in devlist:
        if(dev['0'] == device or dev['1'] == device):
            port = dev['port']
            break #get out of the for loop
    if(port == None):
        #device not connected/found
        return None
    else:
        #init serial connection
        ser = serial.Serial(port, 19200)
        ser.write([data])
        return True #done

def sendCommandToDevice(port, command, extra = None):
    devlist = scanPorts('all')
    connected = False
    for dev in devlist:
        if(dev[0] == port):
            connected = True
            break
    if(connected == False):
        return None #error, not connected


    #define all command functions to generate the serial message to be send
    def sendSettings(port, command, extra = {}):

        #do stuff
        extra = extra #useless assingment to hide annoying msg from IDE ;)
        command = command #ditto
        return {'done':True, 'return':''}
    def getSensorValues(port, command, extra = {}):
        temp = sendCommandToDevice(port, 'getTemperature')
        light = sendCommandToDevice(port, 'getLightLevel')
        return {'done':True, 'return':{'temp':temp, 'light':light}}
    def sendDefaultCmd(port, command, extra = None):
        cmd = getCommandDetails(command)
        if(cmd == None):
            return None #command not found

        msg = [int(cmd['byteCode'],16)]
        i = 0
        while(cmd.get('sendMore', 0) > 0):
            msg.append(extra.get(i, "0x00"))
            cmd['sendMore'] -= 1
            i += 1
        extra = extra #useless assingment to hide annoying msg from IDE ;)
        return {'msg':msg}

    #find out what command we're dealing with
    deviceCommands = {'defaultCmd':sendDefaultCmd, \
    'getSensorValues':getSensorValues}#, \
    #'setSettings':sendSettings}

    data = deviceCommands.get(command, sendDefaultCmd)(port, command, extra)
    if(data == None):
        return None
    if(data.get('done', False)):
        return data['return']

    ser = serial.Serial(port, 19200)
    print(data['msg'])

    ser.write(data['msg'])

    responseCode = ser.read(1)
    response = getCommandDetails(responseCode, 'bytecode')
    if(response['response'] == "FAIL"):
        ser.close()
        return None
    else:
        if(response.get('collectMore') == 1):
            return readByte(ser)
        elif(response.get('collectMore' == 2)):
            return readDoubleByte(ser)
        else:
            ser.close()
            return responseCode


def getCommandDetails(search, searchOn = None):
    configDict = readFromCache(configDir + 'unitcommandsConfig.json', 'dict')

    if(searchOn != None):
        key = searchOn
    else:
        if(len(search) == 4 and search[:2] == "0x"):#bytecode
            key = 'bytecode'
        else:
            key = 'tag'
    for item in configDict:
        if(item[key] == search):
            return item
    return None #nothing found


#using countConnectedDevices automatically updates the devices.json cache
def getConnectedDevicesInfo():
    deviceinfo = scanPorts('all')

    parsedinfo = {}
    i = 0
    for device in deviceinfo:
        parsedinfo[i] = {'port':device[0], \
        'serial':device[1], \
        'description':device[2]}
        i += 1

    writeToCache(cacheDir + "devices.json", parsedinfo)

    return deviceinfo

def initNewDevice(device):#device from scanPorts()
    settingsCache = readFromCache(cacheDir + "deviceSettings.json", 'dict')
    deviceCache = readFromCache(cacheDir + "devices.json", 'dict')

    if((device.serial_number in settingsCache) == False):#if not in cache
        default = readFromCache(configDir + 'settingsConfig.json', 'dict')['default']
        settingsCache[device.serial_number] = settingsCache.get(device.serial_number, default)
        writeToCache(cacheDir + 'deviceSettings.json', settingsCache)

    i = 0
    for dev in deviceCache:
        i += 1
        if(dev['serial'] == device.serial_number):
            return #all done

    #add device to deviceCache
    deviceCache[i] = {'port':device.device, \
        'serial':device.serial_number, \
        'description':device.description}
    writeToCache(cacheDir + 'devices.json', deviceCache)
    return #all done

def isNewDevice(device):#device from scanPorts()
    settingcache = readFromCache(cacheDir + "deviceSettings.json", 'dict')

    if(device.serial_number in settingcache):
        return False
    else:
        return True

#sensor data to Celcius
def tempSensorToC(tempcode):
    return ((tempcode * (5000 / 1024))-500) / 10

#reverse of tempSensorToC
def tempCToSensor(temp):
    return ((temp * 10) + 500) / (5000 / 1024)
