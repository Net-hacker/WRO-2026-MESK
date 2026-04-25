import motor
import config
import numpy as np
import time
from servo import steer

def brain(Objekte):
    while True:
        motor.bewegung(config.speed)
        if Objekte.empty():
            # Versuch ne smoothe Steuerung zu machen
            if config.servo_value != 0 and time.time() - config.last_servo_change > 0.5:
                config.last_servo_change = time.time()
                if config.servo_value > 0:
                    config.servo_value = max(0, config.servo_value - 0.05)
                else:
                    config.servo_value = min(0, config.servo_value + 0.05)
            steer(config.servo_value)
            continue
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
            continue
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
        config.servo_value = ServoMove
        steer(ServoMove)