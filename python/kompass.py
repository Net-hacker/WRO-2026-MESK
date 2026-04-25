import board
import adafruit_bno055
import kaliLaden
import math
import time
import config

i2c = board.I2C()

sensor = adafruit_bno055.BNO055_I2C(i2c, address=0x29)

def calc(angleM):
    angleM = float(angleM)
    print(f"AngleM: {angleM}")
    if angleM > 180:
        angleNew = angleM - 360
        angleExp1 = angleNew + 90
    else:
        angleExp1 = angleM + 90
    angleExp2 = angleM - 90

    return angleExp1, angleExp2

def direction(angle, iter):
    if iter == 3:
        return -1

    kompass = sensor.euler[0]

    print(f"Grad: {kompass}°")
    angleExp1, angleExp2 = calc(angle)
    print(f"Expected: {angleExp1}, {angleExp2}")

    Exp1Diff = math.fabs(angleExp1 - kompass)
    if Exp1Diff > 180:
        Exp1Diff = 360 - Exp1Diff
    Exp2Diff = math.fabs(angleExp2 - kompass)
    if Exp2Diff > 180:
        Exp2Diff = 360 - Exp2Diff
    print(f"Diff: {Exp1Diff}, {Exp2Diff}")
    
    if Exp1Diff < Exp2Diff:
        if Exp1Diff < 50:
            return 1 # Rechts
        else:
            time.sleep(0.5)
            return direction(angle, iter + 1) # try again
    elif Exp1Diff > Exp2Diff:
        if Exp2Diff < 50:
            return 0 # Links
        else:
            time.sleep(0.5)
            return direction(angle, iter + 1) # try again
    else:
        return -1 # ERROR

# Main Program

def startup():
    kaliLaden.load_calibration(sensor)

    # Wartezeit für das Laden der Kalibrierung
    for i in range(0, 3):
        time.sleep(1)

    config.direction = direction(config.angle_value, 0)
    print(f"Richtung: {config.direction}")
