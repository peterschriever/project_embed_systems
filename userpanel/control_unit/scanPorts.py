import serial
import serial.tools.list_ports

def scanPorts():
    ports = []
    for device in serial.tools.list_ports.comports():
        print(device.description)
        if((device.description).find("Arduino Uno") != -1):
            ports.append(device.device)
    return ports
    
print(scanPorts())