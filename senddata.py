# coding=UTF-8
import serial
import time
import numpy as np

x = np.arange(0, 2 * np.pi, 0.1)

ser = serial.Serial('COM3', 115200, timeout=0.05)

while True:
    for i in x:
        #y = np.cos(i)*5+20
        y = np.sin(10*i)*np.exp(-i/2)*10+ 30
        y = '%.2f' % y
        ser.write(y.encode())
        time.sleep(0.1)