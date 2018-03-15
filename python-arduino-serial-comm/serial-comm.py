from time import sleep
import serial
import io
import json
import struct

try:
    arduino = serial.Serial('COM4', 9600)
    sleep(2)
    print("Connection to " + "9600" + " established succesfully!")
except Exception as e:
    print(e)

arduino.write(b'{"brightness":25,"block":"0,12,0,0,0","led":["0,0,0,0"]}')
sleep(2)
res = ''
while arduino.in_waiting:
    res += arduino.readline().decode()
arduino.close()

print(res)
