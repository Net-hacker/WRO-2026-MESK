import config
import RPi.GPIO as GPIO
from gpiozero import PWMLED
from signal import pause
import time

led = PWMLED(27)

def Update():
    while True:
        led.value = config.brightness_value