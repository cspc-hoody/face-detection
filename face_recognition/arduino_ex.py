import serial
import time

ser = serial.Serial('com8', 9600)
time.sleep(2)

id = 1
id = str(id)
print(id)
ser.write(id.encode())
time.sleep(10)
