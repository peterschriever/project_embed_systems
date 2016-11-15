import json
import os
import serial
import serial.tools.list_ports


cacheDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\control_unit\\json_cache\\"
configDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\control_unit\\config\\"

def scanPorts(info = ""):
    ports = []
    for device in serial.tools.list_ports.comports():
        if((device.description).find("Arduino Uno") != -1):
            if(isNewDevice(device)):
                initNewDevice(device)
            if(info == 'all'):
                ports.append([device.device, device.serial_number, device.description])
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
        if(dev.device == port):
            connected = True
            break
    if(connected == False):
        return None #error, not connected
    
    
    #define all command functions to generate the serial message to be send
    def sendSettings(command, extra = {}):
        returnAmount = 8
        #do stuff
        extra = extra #useless assingment to hide annoying msg from IDE ;)
        command = command #ditto
        return {'msg':'test', 'returns':returnAmount}
    def sendDefaultCmd(command, extra = None):
        cmd = getCommandDetails(command)
        if(cmd == None):
            return None #command not found
        
        msg = [cmd['byteCode']]
        i = 0
        while(cmd.get('sendMore', 0) > 0):
            msg.append(extra.get(i,"0x00"))
            cmd['sendMore'] -= 1
            i += 1
        returnAmount = 8 #amount of bytes to read after this msg
        extra = extra #useless assingment to hide annoying msg from IDE ;)
        return {'msg':msg, 'returns':returnAmount}
    
    #find out what command we're dealing with
    deviceCommands = {'defaultCmd':sendDefaultCmd}#, \
    #'setSettings':sendSettings}
    
    data = deviceCommands.get(command, sendDefaultCmd)(command, extra)
    
    ser = serial.Serial(port, 19200)
    ser.write([data['msg']])
    
    if(data['returns'] < 1):
        return None
    else:
        return ser.read(data['returns'])
    
    
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
        newSettingsCache = settingsCache.get(device.serial_number, default)
        writeToCache(configDir + 'settingsConfig.json', newSettingsCache)
    
    i = 0
    for dev in deviceCache:
        i += 1
        if(dev['serial'] == device.serial_number):
            return #all done
        
    #add device to deviceCache
    deviceCache[i] = {'port':device[0], \
        'serial':device[1], \
        'description':device[2]}
    writeToCache(cacheDir + 'devices.json', deviceCache)
    return #all done
    
def isNewDevice(device):#device from scanPorts()
    settingcache = readFromCache(cacheDir + "deviceSettings.json", 'dict')
    
    if(device.serial_number in settingcache):
        return False
    else:
        return True