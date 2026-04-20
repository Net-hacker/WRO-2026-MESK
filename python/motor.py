from gpiozero import PWMOutputDevice, DigitalOutputDevice
import time

# Motor Setup
LPWM = PWMOutputDevice(13)
RPWM = PWMOutputDevice(18)
L_EN = DigitalOutputDevice(23)
R_EN = DigitalOutputDevice(24)

def motor(richtung: str, geschwindigkeit: float):

    L_EN.on()
    R_EN.on()

    if richtung == "rueckwaerts":
        LPWM.value = 0
        RPWM.value = geschwindigkeit

    elif richtung == "vorwaerts":
        LPWM.value = geschwindigkeit
        RPWM.value = 0

def bewegung(geschwindigkeit: float):
    if motor > 0:
        motor("vorwaerts", geschwindigkeit)
    elif motor < 0:
        motor("rueckwaerts", geschwindigkeit)
    else:
        motor_stop()

def motor_stop():
    LPWM.value = 0
    RPWM.value = 0
    L_EN.off()
    R_EN.off()
