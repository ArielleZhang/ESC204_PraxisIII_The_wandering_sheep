import serial
import time



ser = serial.Serial('COM5', baudrate = 115200, timeout = 1)
f = open('readme.txt', 'w')

while True:
    time.sleep(1)
    arduinoData = ser.readline()
    #val = arduinoData.decode("utf-8")
    #str(arduinoData)
    print(arduinoData)
    #f.write(arduinoData)