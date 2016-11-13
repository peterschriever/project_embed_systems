import time
import serial as s

ser = s.Serial('/dev/ttyACM1', 19200)
time.sleep(1)

# read one byte and use ord to make it an int
def read_byte():
    byte = ord(ser.read(1))
    return byte

def read_double():
    byte = (ord(ser.read(1)) << 8)
    byte += ord(ser.read(1))
    return byte

def getTemperature():
    tempCmd = 0xf1


for i in range(0, 50):
    print(read_double())

ser.close()
