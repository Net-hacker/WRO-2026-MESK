import motor
import config
import numpy as np
import time
from servo import steer
import motor
import ultraschall as ultra
import Lasersensor

alert = False

def brain(Objekte):
    global alert
    while True:
        if alert == True:
            servo.steer(0.0)
            motor.bewegung(-0.5)
            time.sleep(0.5)
            alert = False
            ultra.checkStop()
        motor.bewegung(config.speed)
        if Objekte.empty():
            # Versuch ne smoothe Steuerung zu machen
            if config.servo_value != 0 and time.time() - config.last_servo_change > 0.1:
                config.last_servo_change = time.time()
                if config.servo_value > 0:
                    config.servo_value = max(0, config.servo_value - 0.05)
                else:
                    config.servo_value = min(0, config.servo_value + 0.05)
            steer(config.servo_value)
            continue
        ServoMove = Objektwinkel(Objekte)
        if ServoMove is None:
            print("Kein Objekt erkannt, fahre im Kreis")
            links = Lasersensor.vl53_l.range
            rechts = Lasersensor.vl53_r.range
            if (links >= 8000):
                print("Linker Sensor: Kein Signal")
            if (rechts >= 8000):
                print("Rechter Sensor: Kein Signal")

            print(f"Links: {links}mm | Rechts: {rechts}mm")

            if config.direction == 0: # Links
                print("Gehe Links")
                if (links > 2000):
                    print("Links frei, gehe Links")
                    steer(-0.7)
                else:
                    print("Links blockiert")
                    steer(0.2)
            elif config.direction == 1: # Rechts
                print("Gehe Rechts")
                if (rechts > 2000):
                    print("Rechts frei, gehe Rechts")
                    steer(0.7)
                else:
                    print("Rechts blockiert")
                    steer(-0.2)
            elif config.direction == -1: # Kein Wissen Temporär Rechts
                print("Richtung unbekannt, gehe temporär Links")
                if (links > 2000):
                    print("Links frei, gehe Links")
                    steer(-0.7)
                else:
                    print("Links blockiert")
                    steer(0.2)
        if ServoMove is not None:
            config.servo_value = ServoMove
            steer(ServoMove)

def Objektwinkel(Objekte):
    print("Kein Fehler")
    Elemente = Objekte.get()
    groeste_flaeche = 0
    groester_approx = None
    groeste_maske = None
    for approx, flaeche, maske in Elemente:
        if flaeche > groeste_flaeche:
            groeste_flaeche = flaeche
            groester_approx = approx
            groeste_maske = maske
    if groester_approx is None:
        return None
    punkte = groester_approx.reshape(-1, 2)
    mittelpunkt = np.mean(punkte, axis=0) # Mittelpunkt des größen Objektes bestimmen
    # print(mittelpunkt)
    time.sleep(0.1)
    counter = groeste_maske
    print(counter)
    if counter == 0: # Grüne = Links
        ServoMove = -(-0.8*mittelpunkt[0]+480)/600
    elif counter == 1 or counter == 2: # Rote = Rechts
        ServoMove = (0.8* mittelpunkt[0] + 480)/600
    else:
        ServoMove = 0

    print("Mittelpunkt:", mittelpunkt, "ServoMove:", ServoMove)
    return ServoMove
