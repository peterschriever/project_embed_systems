import serial
import time

class ControlUnit:
    BAUD_RATE = 19200

    def __init__(self, port, serial, description):
        self.port = port
        self.serial = serial
        self.description = description

    def __str__(self):
        return "ControlUnit object: " + self.port + ", " + self.serial + \
            ", " + self.description

    def sendCommand(self, unitCmd):
        ser = serial.Serial(self.port, ControlUnit.BAUD_RATE)
        ser.write([unitCmd.byteCode])
        # TODO: rewrite C code base so that it never sends by default
        # and only sends responses to Python code commands
        # this way the Python code can simply wait for the board to reply
        time.sleep(0.1)
        respByte = ord(ser.read(1))
        print("respByte", respByte)
        return respByte
