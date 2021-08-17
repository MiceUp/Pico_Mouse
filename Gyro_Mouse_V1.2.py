import adafruit_mpu6050
import board
import busio
import time
from math import atan2, degrees
import usb_hid
from adafruit_hid.mouse import Mouse
import digitalio




# we need to recalibrate gyro when using gyro with new mouse 
#global vars
zx_calibration = 273
yz_calibration = 269 

Button = digitalio.DigitalInOut(board.GP17)
Button.switch_to_input(pull=digitalio.Pull.DOWN)

Led = digitalio.DigitalInOut(board.GP16)
Led.direction = digitalio.Direction.OUTPUT

i2c = busio.I2C(board.GP15, board.GP14)
mpu = adafruit_mpu6050.MPU6050(i2c)
m = Mouse(usb_hid.devices)

Led_state = False 


def vector_2_degrees(x, y):
    angle = degrees(atan2(y, x))
    if angle < 0:
        angle += 360
    return angle

def get_inclination(_sensor):
    x, y, z = _sensor.acceleration
    return (vector_2_degrees(x, z) - zx_calibration), (vector_2_degrees(y, z) - yz_calibration) 


while True:
    Led.value = Led_state
    angle_xz, angle_yz = get_inclination(mpu)
    # print("XZ angle = {:6.2f}deg YZ angle = {:6.2f}deg".format(angle_xz , angle_yz))
    
    # LED and Button Testing
    if (Button.value):
        print("button pressed")
        if (Led_state == False):
            Led_state = True
            m.press(Mouse.LEFT_BUTTON)
        else: 
            Led_state = False
            m.release_all()
            
        time.sleep(0.2)
        # do a left click mouse press press down    
        # Gyro Testing
    elif(angle_yz > 16):
        m.click(Mouse.LEFT_BUTTON)
        print("Left Click")
        Led.value = True
        time.sleep(0.75)
        Led.value = False
        print("Left Release")
    elif(angle_yz < -16):
        m.click(Mouse.RIGHT_BUTTON)
        print("Right Click")
        time.sleep(0.75)
        print("Right Release")
    elif (angle_xz > 20):
        m.move(wheel=+1)
        print("Scrolling Forward")
        time.sleep(0.1)
    elif (angle_xz <  -20):
        m.move(wheel=-1)
        print("Scrolling Backward")
        time.sleep(0.1)
    