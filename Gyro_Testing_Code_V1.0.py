

import adafruit_mpu6050
import board
import busio
import time
from math import atan, degrees, sqrt

i2c = busio.I2C(board.GP15, board.GP14)
mpu = adafruit_mpu6050.MPU6050(i2c)
pitch = 0;
roll = 0;

def getAngle(gyro):
    Ax, Ay, Az = gyro.acceleration
    print("Ax: "+ str(Ax))
    print("Ay: "+ str(Ay))
    print("Az: "+ str(Az))
    
    pitch = atan(Ax/ sqrt((Ay*Ay) + (Az*Az)))
    roll = atan(Ay/ sqrt((Ax*Ax) + (Az*Az)))


while True:
    #print("Acceleration: X:%.2f, y: %.2f, Z: %.2f m/s^2" % (mpu.acceleration))
    print("Gyro: X:%.2f, y: %.2f, Z: %.2f Degrees" % (mpu.gyro))
    print("Temp: %.2f C " % mpu.temperature)
   
    
    getAngle(mpu)
    print(pitch)
    print(roll)
    print("") 
    
    
    time.sleep(0.25)
