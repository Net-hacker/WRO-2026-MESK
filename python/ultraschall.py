from gpiozero import DistanceSensor
from time import sleep

links = DistanceSensor(echo=21, trigger=20)
rechts = DistanceSensor(echo=26, trigger=16)

try:
    print("rechts" + rechts*100 + "links" + links*100)

except KeyboardInterrupt:
    pass