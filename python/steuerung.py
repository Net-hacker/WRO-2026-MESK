import motor
import config
import numpy as np
import time
import servo
import motor
import ultraschall as ultra
import Lasersensor

alert = False
lastObjekttime = 0
lastObjektPosition = None # None = Zu lange her, -1 = Links, 1 = Rechts

def brain(Objekte):
    global alert
    config.speed = 0
    while True:
        if alert == True:
            servo.steer(0.0)
            motor.bewegung(-0.5)
            time.sleep(0.5)
            alert = False
        motor.bewegung(config.speed)
        ServoMove = Objektwinkel(Objekte)
        if ServoMove is None:
            # print("Kein Objekt erkannt, fahre im Kreis")
            links = Lasersensor.average_left
            rechts = Lasersensor.average_right

            # print(f"Links: {links}mm | Rechts: {rechts}mm")

            if config.direction == 0: # Links
                InDirection = links
                AntiDirection = rechts
            elif config.direction == 1: # Rechts
                InDirection = rechts
                AntiDirection = links
            elif config.direction == -1: # Kein Wissen Temporär Rechts
                print("Richtung unbekannt, gehe temporär Rechts")
                InDirection = rechts
                AgainDirection = links

            ServoInDirection = (1.4 * InDirection + 480) / 600 - 1
            print("Right: ", Lasersensor.vl53_r.range, "    Left: ", Lasersensor.vl53_l.range, "   ServoInDirection:", InDirection)
            print(f"ServoInDirection: {InDirection}")

            if config.direction == 0: # Links
                ServoMove = -ServoInDirection
            elif config.direction == 1: # Rechts
                ServoMove = ServoInDirection
            elif config.direction == -1: # Kein Wissen Temporär Rechts
                ServoMove = ServoInDirection
            global lastObjekttime, lastObjektPosition
            if time.time() - lastObjekttime < 1:
                print("Kein Objekt mehr in Sicht")
                if abs(ServoMove + lastObjektPosition) < 1:
                    print("Verhindere fahren gegen das Objekt")
                    servo.steer(0)
                    continue
                print("Objekt nicht mehr in Sicht, aber ServoMove nicht in Richtung des letzten Objekts, gehe weiter")
            else:
                print("Objekt zu lange her, gehe im Kreis")
                lastObjektPosition = None
            servo.steer(ServoMove)
        else:
            # print(f"Objekt erkannt, ServoMove: {ServoMove}")
            config.servo_value = ServoMove
            servo.steer(ServoMove)

def Objektwinkel(Objekte):
    #global lastMask, timestamp, blockMovement
    # print("Kein Fehler")
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
        #if time.time() - timestamp < 0.5:
        #    blockMovement = True
        return None
    punkte = groester_approx.reshape(-1, 2)
    mittelpunkt = np.mean(punkte, axis=0) # Mittelpunkt des größen Objektes bestimmen
    global lastObjektPosition, lastObjekttime
    if mittelpunkt[0] < 300:
        lastObjektPosition = -1
    else:
        lastObjektPosition = 1
    lastObjekttime = time.time()
    # print("Objekt erkannt, lastObjektPosition:", lastObjektPosition, "lastObjekttime:", lastObjekttime, "counter:", groeste_maske)
    # print(mittelpunkt)
    time.sleep(0.1)
    counter = groeste_maske
    if counter == 0: # Grüne = Links
        ServoMove = -(-0.8 * mittelpunkt[0]+480)/600
    elif counter == 1 or counter == 2: # Rote = Rechts
        ServoMove = (0.8 * mittelpunkt[0] + 480)/600
    else:
        ServoMove = 0
    return ServoMove
