import numpy as np
import os
try:
    from motor import bewegung
    from servo import steer
except ImportError:
    pass
import time

mode = True # Konfiguration um Systemweite Kameramodus zu haben

# [0] == Maske 1; [1] == Maske 2; [2] == Maske 3
mask_values = [
    [np.array([0, 0, 0]), np.array([0, 0, 0])],
    [np.array([0, 0, 0]), np.array([0, 0, 0])],
    [np.array([0, 0, 0]), np.array([0, 0, 0])]
]

# [0] == Maske 1; [1] == Maske 2; [2] == Maske 3
tolerance_values = [
    0, 0, 0
]

# [0] == Maske 1; [1] == Maske 2; [2] == Maske 3
angle_values = [
    0, 0, 0
]

# [0] == Links; [1] == Rechts
ultra_values = [
    0, 0
]

motor_value = 0

servo_value = 0

last_servo_change = time.time()

def startup():
    try:
        steer(0)
        # bewegung(0.2)
    except:
        pass

    for m in range(len(mask_values)): # Ufbassa, ob das richtig ist??
        upper, lower = load_preset(m)
        mask_values[m] = [upper, lower]

    for t in range(len(tolerance_values)):
        tolerance = load_tolerance(t)
        tolerance_values[t - 1] = tolerance

    for a in range(len(angle_values)):
        angle = load_angle(a)
        angle_values[a - 1] = angle

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

def load_angle(id):
    if not os.path.exists("Preset/"):#
        return 0

    try:
        with open(f"Preset/{id}_Angle.txt", "r") as file:
            angle = file.read()
            file.close()
    except:
        return 0

    return angle
