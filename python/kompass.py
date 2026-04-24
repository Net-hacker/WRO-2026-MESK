import board
import adafruit_bno055
import kaliBinLaden
import math

i2c = board.I2C()

sensor = adafruit_bno055.BNO055_I2C(i2c, address=0x29)

def calc(angleM, angleR):
    return round(math.sin(angleM - angleR))

def direction(angle):
    Cock = sensor.euler[0]

    print(f"Penisgrad: {Cock}°")
    print(calc(angle, Cock))

kaliBinLaden.load_calibration(sensor)

while True:
    direction(0)
