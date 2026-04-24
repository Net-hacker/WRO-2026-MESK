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
# Wir nutzen die Library direkt mit der Default-Adresse zum Umstellen
i2c.writeto(0x29, bytes([0x8A, 0x30])) 
time.sleep(0.1)
print("Sensor 1 auf 0x30 bereit.")

xshut2.value = True
time.sleep(0.2)
# Wichtig: Hier jetzt VL53L0X(i2c) aufrufen, da der neue Sensor auf 0x29 wartet
i2c.writeto(0x29, bytes([0x8A, 0x31])) 
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
    time.sleep(0.2)

# 3. DER TRICK: Adresse ändern, bevor das VL53L0X-Objekt erstellt wird
# Wir schicken einen direkten I2C-Befehl an die 0x29, um sie auf 0x30 zu ändern.
# Das Register für die Adresse beim VL53L0X ist 0x8A.
try:
    # Wir schreiben direkt in das Register 0x8A des Geräts an 0x29
    i2c.writeto(0x29, bytes([0x8A, 0x30])) 
    time.sleep(0.1)
    print("Adresse hardwareseitig auf 0x30 erzwungen.")
except Exception as e:
    print(f"Direkt-Schreiben fehlgeschlagen: {e}")

# 4. Erst JETZT die Library laden, aber direkt auf der NEUEN Adresse suchen
from adafruit_vl53l0x import VL53L0X
try:
    vl53 = VL53L0X(i2c, address=0x30)
    print("Laser-Sensor erfolgreich auf 0x30 initialisiert!")
except Exception as e:
    print(f"Initialisierungsfehler: {e}")

# 5. Jetzt kannst du den BNO055 dazuholen (er ist jetzt allein auf 0x29)
# bno = adafruit_bno055.BNO055_I2C(i2c)

while True:
    print(f"Abstand: {vl53.range} mm")
    time.sleep(0.5)