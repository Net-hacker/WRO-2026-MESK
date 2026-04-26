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
last_error = 0

# Parameter (empirisch tunen)
BIAS = 0.4          # Grundkurve in Fahrtrichtung
Kp = 0.0045            # Proportionalanteil
Kd = 0.0023            # Dämpfung
TARGETID = 430         # Sollabstand zur Innenbande in mm (rechter Sensor)
TARGETAG = 190         # Sollabstand zur Außenbande in mm (linker Sensor)
ServoInDirection = BIAS # Fallback

def brain(Objekte):
    global alert
    config.speed = 0.3#7
    while True:
        if alert == True:
            servo.steer(0.0)
            motor.bewegung(-0.5)
            time.sleep(1)
            alert = False
        motor.bewegung(config.speed)
        ObjektServo, fläche = Objektwinkel(Objekte)
        # sServoMove = None #TEMP
        LaserServo = Laser()
            # print("Kein Objekt erkannt, fahre im Kreis")
        print(f"ObjektServo: {ObjektServo}, LaserServo: {LaserServo}, Fläche: {fläche}")
        if ObjektServo is None:
            ServoMove = LaserServo 
            global lastObjekttime, lastObjektPosition
            if time.time() - lastObjekttime < -1.5 * (config.speed - 1): 
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
            ServoMove = ObjektServo * min(1, fläche / 10000) + LaserServo * max(0, 1- fläche / 10000)
            # print(f"Objekt erkannt, ServoMove: {ServoMove}")
            config.servo_value = ServoMove
            servo.steer(ServoMove)

def Laser():
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
        # print("Richtung unbekannt, gehe temporär Rechts")
        InDirection = rechts
        AntiDirection = links

    global last_error, BIAS, Kp, Kd, TARGETID, TARGETAG, ServoInDirection
    errorID = TARGETID - InDirection
    errorAG = AntiDirection - TARGETAG
    total_conf = Lasersensor.confidence_right +  Lasersensor.confidence_left
    if total_conf > 0:
        error = (Lasersensor.confidence_right * errorID + Lasersensor.confidence_left * errorAG) / total_conf
    else:
        error = 0
    error = error if config.direction == 1 else -error
    MAX_D_ERROR = 50
    d_error = max(-MAX_D_ERROR, min(MAX_D_ERROR, error - last_error))
    last_error = error

    ServoInDirection = BIAS + Kp * error + Kd * d_error
    ServoInDirection = max(-1.0, min(1.0, ServoInDirection)) # Begrenze den ServoMove auf [-1, 1]

    print(f"std_l={np.std(Lasersensor.left_values):.0f}  std_r={np.std(Lasersensor.right_values):.0f}  conf_l={Lasersensor.confidence_left:.2f}  conf_r={Lasersensor.confidence_right:.2f}")
    print(f"ID={Lasersensor.average_right}  AD={Lasersensor.average_left}")
    print("Right: ", Lasersensor.vl53_r.range, "    Left: ", Lasersensor.vl53_l.range, "   ServoInDirection:", ServoInDirection)
    print(f"errorID={errorID:.0f}  errorAG={errorAG:.0f}  error={error:.0f}  conf_r={Lasersensor.confidence_right:.2f}  conf_l={Lasersensor.confidence_left:.2f}")

    if config.direction == 0: # Links
        ServoMove = -ServoInDirection
    elif config.direction == 1: # Rechts
        ServoMove = ServoInDirection
    elif config.direction == -1: # Kein Wissen Temporär Rechts
        ServoMove = ServoInDirection
    return ServoMove

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
        return None, 0
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
    return ServoMove, groeste_flaeche
