import numpy as np
import os
import time
from gpiozero import PWMLED
import kompass


Rennen = 1 # 1= Eröffnung, 0 = Hinderniss

mode = True # Konfiguration um Systemweite Kameramodus zu haben

# ANLEITUNG ZUM HINZUFÜGEN NEUER MASKEN:
# - Bei mask_values eine neue Zeile hinzufügen
# - Bei tolerance_values einen neuen Wert hinzufügen
# - In Objekterkennung.py in der Funktion toKonturen die if-Abfrage erweitern


# [0] == Maske 1; [1] == Maske 2; [2] == Maske 3
mask_values = [
    [np.array([0, 0, 0]), np.array([0, 0, 0])],
    [np.array([0, 0, 0]), np.array([0, 0, 0])],
    [np.array([0, 0, 0]), np.array([0, 0, 0])],
    [np.array([0, 0, 0]), np.array([0, 0, 0])],
    [np.array([0, 0, 0]), np.array([0, 0, 0])]
]

# [0] == Maske 1; [1] == Maske 2; [2] == Maske 3
tolerance_values = [
    0, 0, 0, 0, 0
]

angle_value = 0 # Richtung der Matte

# [0] == Links; [1] == Rechts
ultra_values = [
    0, 0
]

speed = 0

servo_value = 0

brightness_value = 0

last_servo_change = time.time()

direction = -1 # Richtung in die der Lauf geht. -1 = kein Wissen, 0 = Links, 1 = Rechts

led = PWMLED(27)

STARTUP_GELADEN = False

def startup():
    for m in range(len(mask_values)): # Ufbassa, ob das richtig ist??
        upper, lower = load_preset(m)
        if upper is not None and lower is not None:
            mask_values[m] = [upper, lower]

    for t in range(len(tolerance_values)):
        tolerance = load_tolerance(t)
        tolerance_values[t - 1] = tolerance

    global angle_value, brightness_value, STARTUP_GELADEN
    
    angle_value = load_angle()
    kompass.startup()
    brightness_value = load_brightness()
    STARTUP_GELADEN = True




if STARTUP_GELADEN:
    import kompass
    try:
        from motor import bewegung
        from servo import steer
    except ImportError:
        pass

def load_preset(id):
    if not os.path.exists("Preset/"):
        return None, None

    try:
        with open(f"Preset/{id}_Preset.txt", "r") as file:
            content = file.read()
            file.close()
    except:
        return None, None

    werte = [int(w.strip()) for w in content.split(",")]

    lower = np.array(werte[:3])
    upper = np.array(werte[3:])

    return upper, lower

def load_tolerance(id):
    if not os.path.exists("Preset/"):
        return 0.2

    try:
        with open(f"Preset/{id}_Tolerance.txt", "r") as file:
            tolerance = file.read()
            file.close()
    except:
        return 0.2

    return tolerance

def load_angle():
    if not os.path.exists("Preset/"):
        return 0

    try:
        with open(f"Preset/Angle.txt", "r") as file:
            angle = file.read()
            file.close()
    except:
        return 0

    return angle

def load_brightness():
    if not os.path.exists("Preset/"):
        return 0

    try:
        with open("Preset/Bright.txt", "r") as file:
             bright = file.read()
             file.close()
    except:
        return 0

    return bright

def UpdateLED():
    global led
    led.value = min(1, float(brightness_value))