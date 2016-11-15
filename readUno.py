import time
import serial as s

ser = s.Serial('/dev/ttyACM0', 19200)
time.sleep(1)

# read one byte and use ord to make it an int
def read_byte():
    byte = ord(ser.read(1))
    return byte

def read_double():
    firstByte = (ord(ser.read(1)) << 8)
    secondByte = (ord(ser.read(1)))
    return firstByte + secondByte

def read_unknown():
    # @TODO: some kind of thing to sync up
    # (only if it is really needed in the future)
    idByte = ser.read(1)
    if ord(idByte) == ord(b'T'):
        temp = read_byte()
        temp *= (5000.0/1024)
        temp -= 500
        temp /= 10
        return "Temp: "+str(temp)
    else:
        return "Light: "+str(read_double())

for i in range(0, 500):
    # temp = read_byte()
    # temp *= (5000.0/1024)
    # temp -= 500
    # temp /= 10
    # print(temp)
    print(read_unknown())
    time.sleep(.30)

ser.close()
