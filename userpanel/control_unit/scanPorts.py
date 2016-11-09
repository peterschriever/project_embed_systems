import serial
import serial.tools.list_ports

def scanPorts(info=""):
    ports = []
    for device in serial.tools.list_ports.comports():
        if((device.description).find("Arduino Uno") != -1):
            if(info == 'all'):
                ports.append([device.device, device.serial_number, device.description])
            else:
                ports.append(device.device)
    return ports
    