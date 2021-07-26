import adafruit_mpu6050
import board
import busio
import time
from math import atan2, degrees
import usb_hid
from adafruit_hid.mouse import Mouse

# we need to recalibrate gyro when using gyro with new mouse 
#global vars
zx_calibration = 92
yz_calibration = 88

i2c = busio.I2C(board.GP15, board.GP14)
mpu = adafruit_mpu6050.MPU6050(i2c)
m = Mouse(usb_hid.devices)


def vector_2_degrees(x, y):
    angle = degrees(atan2(y, x))
    if angle < 0:
        angle += 360
    return angle

def get_inclination(_sensor):
    x, y, z = _sensor.acceleration
    return (vector_2_degrees(x, z) - zx_calibration), (vector_2_degrees(y, z) - yz_calibration) 


while True:
    angle_xz, angle_yz = get_inclination(mpu)
    print("XZ angle = {:6.2f}deg YZ angle = {:6.2f}deg".format(angle_xz , angle_yz))
    
    if(angle_yz > 16):
        m.click(Mouse.LEFT_BUTTON)
        print("Left Click")
        time.sleep(0.3)
        print("Left Release")
    elif(angle_yz < -16):
        m.click(Mouse.RIGHT_BUTTON)
        print("Right Click")
        time.sleep(0.3)
        print("Right Release")
    elif (angle_xz > 20):
        m.move(wheel=+1)
        print("Scrolling Forward")
    elif (angle_xz <  -20):
        m.move(wheel=-1)
        print("Scrolling Backward")
        
    
        
    
    
    time.sleep(0.2)
