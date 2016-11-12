import serial.tools.list_ports
import functions.initNewDevice
import functions.isNewDevice

def scanPorts(info=""):
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
    