from gpiozero import PWMOutputDevice, DigitalOutputDevice
import time

# Motor Setup
LPWM = PWMOutputDevice(13)
RPWM = PWMOutputDevice(18)
L_EN = DigitalOutputDevice(23)
R_EN = DigitalOutputDevice(24)

def motor(richtung, geschwindigkeit):

    L_EN.on()
    R_EN.on()

    if richtung == "vorwaerts":
        LPWM.value = 0
        RPWM.value = geschwindigkeit

    elif richtung == "rueckwaerts":
        LPWM.value = geschwindigkeit
        RPWM.value = 0

def motor_stop():
    LPWM.value = 0
    RPWM.value = 0
    L_EN.off()
    R_EN.off()
