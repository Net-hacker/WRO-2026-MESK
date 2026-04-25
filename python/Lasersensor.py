import time
import board
import digitalio
import servo
import config
import motor

def Scan():
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

    from adafruit_vl53l0x import VL53L0X
    try:
        vl53_r = VL53L0X(i2c, address=0x30)
        vl53_r.measurement_timing_budget = 200000
        vl53_r.signal_rate_limit = 0.1
        print("Laser-Sensor erfolgreich auf 0x30 initialisiert!")
    except Exception as e:
        print(f"Initialisierungsfehler: {e}")

    try:
        vl53_l = VL53L0X(i2c, address=0x31)
        vl53_l.measurement_timing_budget = 200000
        vl53_l.signal_rate_limit = 0.1
        print("Laser-Sensor erfolgreich auf 0x31 initialisiert!")
    except Exception as e:
        print(f"Initialisierungsfehler: {e}")

    while True:
        yield(vl53_l.range, vl53_r.range)
        time.sleep(0.1)

motor.bewegung(0.2)
for links, rechts in Scan():

    if (links >= 8000):
        print("Linker Sensor: Kein Signal")
    if (rechts >= 8000):
        print("Rechter Sensor: Kein Signal")

    print(f"Links: {links}mm | Rechts: {rechts}mm")

    if config.direction == 0: # Links
        print("Gehe Links")
    elif config.direction == 1: # Rechts
        print("Gehe Rechts")
    elif config.direction == -1: # Kein Wissen Temporär Rechts
        print("Richtung unbekannt, gehe temporär Links")
        if (links > 2000):
            print("Links frei, gehe Links")
            servo.steer(-0.7)
        else:
            print("Links blockiert")
            servo.steer(0.2)