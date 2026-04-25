import time
import board
import adafruit_bno055
import sys
import os

# Füge das Hauptverzeichnis (WRO-2026-MESK/python) zum Suchpfad hinzu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import Lasersensor  # Jetzt findet er die Lasersensor.py im Hauptordner
Lasersensor.Configure_I2C()
# I2C Verbindung aufbauen
i2c = board.I2C() 
# WICHTIG: Hier die 0x29 eintragen, die wir bei i2cdetect gesehen haben
sensor = adafruit_bno055.BNO055_I2C(i2c, address=0x29)

print("BNO055 Test gestartet. Bewege den Sensor!")

while True:
    # Euler-Winkel auslesen (Heading, Roll, Pitch)
    # Heading ist der Kompass-Wert (0-360 Grad)
    heading, roll, pitch = sensor.euler
    
    print(f"Ausrichtung: Heading={heading:.2f}° | Roll={roll:.2f}° | Pitch={pitch:.2f}°")
    
    # Kalibrierungsstatus (0=schlecht, 3=perfekt)
    sys, gyro, accel, mag = sensor.calibration_status
    print(f"Kalibrierung: Sys={sys} Gyro={gyro} Accel={accel} Mag={mag}")
    print("-" * 50)
    
    time.sleep(0.5)