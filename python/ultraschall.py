from gpiozero import DistanceSensor
from time import sleep

sensorlinks = DistanceSensor(echo=21, trigger=20)
sensorrechts = DistanceSensor(echo=26, trigger=16)


def readsensor():

    distli = sensorlinks.distance * 100
    distre = sensorrechts.distance * 100
    
    return distli-distre
