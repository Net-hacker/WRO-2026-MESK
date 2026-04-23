


def brain(Objekte):
    while True:
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
        elif counter == 1: # Rote = Rechts
            ServoMove = (0.8* mittelpunkt[0] + 480)/600
        else:
            ServoMove = 0

        print("Mittelpunkt:", mittelpunkt, "ServoMove:", ServoMove)