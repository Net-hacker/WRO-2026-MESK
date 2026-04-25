import time
import board
import digitalio
import busio

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
print("Sensor 1 auf 0x30 bereit.")

xshut2.value = True
time.sleep(0.2)
i2c.writeto(0x29, bytes([0x8A, 0x31])) # Adresse des zweiten Sensors auf 0x31 setzen
time.sleep(0.1)
print("Sensor 2 auf 0x31 bereit.")

from adafruit_vl53l0x import VL53L0X
try:
    vl53_1 = VL53L0X(i2c, address=0x30)
    print("Laser-Sensor erfolgreich auf 0x30 initialisiert!")
except Exception as e:
    print(f"Initialisierungsfehler: {e}")

try:
    vl53_2 = VL53L0X(i2c, address=0x31)
    print("Laser-Sensor erfolgreich auf 0x31 initialisiert!")
except Exception as e:
    print(f"Initialisierungsfehler: {e}")


while True:
    print(f"L1: {vl53_1.range}mm | L2: {vl53_2.range}mm")
    time.sleep(0.1)