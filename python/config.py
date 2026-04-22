import numpy as np
import os
from motor import bewegung

mode = True # Konfiguration um Systemweite Kameramodus zu haben

mask_values = [
    [np.array([0, 0, 0]), np.array([0, 0, 0])],
    [np.array([0, 0, 0]), np.array([0, 0, 0])],
    [np.array([0, 0, 0]), np.array([0, 0, 0])]
]

tolerance_values = [
    0, 0, 0
]

def startup():
    bewegung(0.1)

    for m in range(len(mask_values)):
        upper, lower = load_preset(m)
        mask_values[m] = [upper, lower]

    for t in range(len(tolerance_values)):
        tolerance = load_tolerance(t)
        tolerance_values[t] = tolerance

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
        return None

    try:
        with open(f"Preset/{id}_Tolerance.txt", "r") as file:
            tolerance = file.read()
            file.close()
    except:
        return None

    return tolerance
