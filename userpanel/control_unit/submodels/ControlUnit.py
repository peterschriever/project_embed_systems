import serial
import time
from control_unit.submodels.CommandIdentifier import *

class ControlUnit:
    BAUD_RATE = 19200

    def __init__(self, port, serial, description):
        self.port = port
        self.serial = serial
        self.description = description

    def __str__(self):
        return "ControlUnit object: " + self.port + ", " + self.serial + \
            ", " + self.description

    def sendSetCommand(self, unitCmds, cmdsData):
        # if unitCmds is not a list, simply make a list with one item
        if not isinstance(unitCmds, list):
            unitCmds = [unitCmds]

        result = {}
        try:
            ser = serial.Serial(self.port, ControlUnit.BAUD_RATE)

            time.sleep(3) # wait until the serial connection is synced

            for unitCmd in unitCmds:
                # print("unitCmd.byteCode", unitCmd.byteCode)
                ser.write([unitCmd.byteCode])

                send = unitCmd.sendMore
                while send:
                    # send another byte of data, write msb first
                    send -= 1
                    ser.write([(cmdsData[unitCmd.tag] >> (8*send)) & 0xff])
                    print("ser.write", unitCmd.tag, (cmdsData[unitCmd.tag] >> (8*send)) & 0xff)

                responseByteCode = hex(ord(ser.read(1))) # read responseByteCode
                responseCmd = CommandIdentifier.getResponse(responseByteCode)
                # @TODO: check if responseCmd is OK / FAIL
                # for now assume OK
                # print("responseCmd", responseCmd)
                collect = responseCmd.collectMore
                respBytes = []
                while collect:
                    collect -= 1
                    respBytes.append(ord(ser.read(1)) << 8 * collect)
                # print("respBytes", respBytes)

                result[unitCmd.tag] = 0
                # NOTE: probably a better way, without looping, exists for this
                for key in range(0, len(respBytes)):
                    result[unitCmd.tag] += respBytes[key]

                if result[unitCmd.tag] == 0 and responseCmd.response == "OK":
                    result[unitCmd.tag] = 1 # signal that response was succesful
            # print("result", result)
        except Exception as e:
            result = {}
        finally:
            ser.close() # close serial
            return result


    def sendGetCommand(self, unitCmds):
        # if unitCmds is not a list, simply make a list with one item
        if not isinstance(unitCmds, list):
            unitCmds = [unitCmds]

        result = {}
        try:
            ser = serial.Serial(self.port, ControlUnit.BAUD_RATE)

            time.sleep(3) # wait until the serial connection is synced

            for unitCmd in unitCmds:
                print("unitCmd.byteCode", unitCmd.byteCode)
                ser.write([unitCmd.byteCode])
                responseByteCode = hex(ord(ser.read(1))) # read responseByteCode
                responseCmd = CommandIdentifier.getResponse(responseByteCode)
                # @TODO: check if responseCmd is OK / FAIL
                # for now assume OK
                # print("responseCmd", responseCmd)
                collect = responseCmd.collectMore
                respBytes = []
                while collect:
                    collect -= 1
                    respBytes.append(ord(ser.read(1)) << 8 * collect)
                # print("respBytes", respBytes)

                result[unitCmd.tag] = 0
                # NOTE: probably a better way, without looping, exists for this
                for key in range(0, len(respBytes)):
                    result[unitCmd.tag] += respBytes[key]
            # print("result", result)
        except Exception as e:
            result = {}
        finally:
            ser.close() # close serial
            return result
