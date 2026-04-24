import board
import adafruit_bno055
import kaliLaden
import math

i2c = board.I2C()

sensor = adafruit_bno055.BNO055_I2C(i2c, address=0x29)

def calc(angleM):
    if angleM > 180:
        angleNew = angleM - 360
        if angleNew < -90 || angleNew > 90:
            print("ES KRACHT!!!")
            return 0.0, 0.0
        angleExp1 = angleNew + 90
    else:
        angleExp1 = angleM + 90
    angleExp2 = angleM - 90

    return angleExp1, angleExp2

def direction(angle):
    kompass = sensor.euler[0]

    print(f"Grad: {kompass}°")
    angleExp1, angleExp2 = calc(angle)
    print(f"Expected: {angleExp1}, {angleExp2}")

    if math.abs(angleExp1 - kompass) > math.abs(angleExp2 - kompass):
        return 1 # Rechts
    elif math.abs(angleExp1 - kompass) < math.abs(angleExp2 - kompass):
        return 0 # Links
    else:
        return -1 # ERROR

# Main Program

kaliLaden.load_calibration(sensor)

for i in range(0, 3):
    time.sleep(1)

direction(0)
