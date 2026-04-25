from gpiozero import DistanceSensor
import config
import time
import motor
import servo

sLinks = DistanceSensor(echo=21, trigger=20)
sRechts = DistanceSensor(echo=26, trigger=16)

def ultraRead():
    distL = sLinks.distance * 100
    distR = sRechts.distance * 100

    if distL != 100 and config.ultra_values[0] != 100:
        config.ultra_values[0] = distL
    if distR != 100 and config.ultra_values[1] != 100:
        config.ultra_values[1] = distR

    print(f"Ultra Links: {distL}  Ultra Rechts: {distR}")
    return distL, distR

def checkStop():
    while True:
        distL, distR = ultraRead()
        border = 70 * config.speed
        if distL <= border or distR <= border:
            distLNew, distRNew = ultraRead()
            if distLNew < distL or distRNew < distR:
                # motor.bewegung(0.0)
                # time.sleep(0.5)
                servo.steer(0.0)
                motor.bewegung(-0.5)
                time.sleep(0.5)
                return 1
        else:
            time.sleep(0.1)

servo.steer(0.0)
motor.bewegung(0.5)
checkStop()
