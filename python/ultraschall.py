from gpiozero import DistanceSensor
import config
import time

sLinks = DistanceSensor(echo=21, trigger=20)
sRechts = DistanceSensor(echo=26, trigger=16)

def ultraRead():
    while True:
        distL = sLinks.distance * 100
        distR = sRechts.distance * 100
        if distL == 100 and config.ultra_values[0] == 100:
            continue
        else:
            config.ultra_values[0] = distL
        if distR == 100 and config.ultra_values[1] == 100:
            continue
        else:
           config.ultra_values[1] = distR
        print("Ultra Links: ", distL, "  Ultra Rechts: ", distR, )
        time.sleep(0.1)

# ultraRead()