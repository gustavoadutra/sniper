import serial
# from dynamixel_sdk import *

opencr = serial.Serial(port='COM3', baudrate=115200)
opencr.write(b'1')
opencr.close()
