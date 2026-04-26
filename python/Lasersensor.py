import time
import board
import digitalio
from collections import deque
import numpy as np


vl53_r, vl53_l = None, None

left_values = deque(maxlen=5)
right_values = deque(maxlen=5)
average_left = 0
average_right = 0
confidence_left = 0.5
confidence_right = 0.5
stable_left = 0
stable_right = 0

def Configure_I2C():
    # 1. Pins vorbereiten
    xshut1 = digitalio.DigitalInOut(board.D4)
    xshut2 = digitalio.DigitalInOut(board.D17)
    xshut1.direction = digitalio.Direction.OUTPUT
    xshut2.direction = digitalio.Direction.OUTPUT

    # Laser GANZ AUS
    xshut1.value = False
    xshut2.value = False
    time.sleep(0.2)

    # I2C Bus starten
    i2c = board.I2C()

    # 2. Den Laser aufwecken
    xshut1.value = True
    time.sleep(0.2)
    i2c.writeto(0x29, bytes([0x8A, 0x30])) # Adresse des ersten Sensors auf 0x30 setzen
    time.sleep(0.1)
    print("Rechter Sensor auf 0x30 bereit.")

    xshut2.value = True
    time.sleep(0.2)
    i2c.writeto(0x29, bytes([0x8A, 0x31])) # Adresse des zweiten Sensors auf 0x31 setzen
    time.sleep(0.1)
    print("Linker Sensor auf 0x31 bereit.")

    global vl53_r, vl53_l
    
    from adafruit_vl53l0x import VL53L0X
    try:
        vl53_r = VL53L0X(i2c, address=0x30)
        vl53_r.measurement_timing_budget = 50000
        vl53_r.signal_rate_limit = 0.1
        print("Laser-Sensor erfolgreich auf 0x30 initialisiert!")
    except Exception as e:
        print(f"Initialisierungsfehler: {e}")

    try:
        vl53_l = VL53L0X(i2c, address=0x31)
        vl53_l.measurement_timing_budget = 50000
        vl53_l.signal_rate_limit = 0.1
        print("Laser-Sensor erfolgreich auf 0x31 initialisiert!")
    except Exception as e:
        print(f"Initialisierungsfehler: {e}")

def compute_confidence(buffer, scale=150):
    values = list(buffer)[-5:]
    if len(values) < 2:
        return 0.0
    std = np.std(values)
    return 1.0 / (1.0 + std / scale) # Schritt 2

def Scan_Worker():
    while True:
        global left_values, right_values, average_left, average_right, confidence_left, confidence_right, stable_left, stable_right
        left = vl53_l.range
        right = vl53_r.range
        if (left >= 8000):
            left = stable_left + 300
        else:
            stable_left = left
        if (right >= 8000):
            right = stable_right + 300
        else:
            stable_right = right
        left_values.appendleft(left)
        right_values.appendleft(right)
        average_left = sum(left_values) // len(left_values)
        average_right = sum(right_values) // len(right_values)
        confidence_left  = compute_confidence(left_values)
        confidence_right = compute_confidence(right_values)
        time.sleep(0.1)