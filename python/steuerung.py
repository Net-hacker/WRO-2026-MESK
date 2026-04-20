# Code zur Steuerung des Fahrt(richtung) anhand der Kamera & den Sensoren
import cv2
import numpy as np

def toKonturen(res_frames, Konturen):
    while True:
        result = res_frames.get()
        grau = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

        # Konturen aus dem Bild extrahieren
        konturen, hierarchy = cv2.findContours(
            grau,
            cv2.RETR_EXTERNAL,    # nur äußere Konturen
            cv2.CHAIN_APPROX_SIMPLE  # komprimierte Darstellung
        )
        Elemente = []
        for k in konturen:
            flaeche = cv2.contourArea(k)
            if flaeche < 20000:
                continue  # Rauschen ignorieren
           

            # Kontur annähern (epsilon = Toleranz)
            epsilon = 0.04 * cv2.arcLength(k, closed=True)
            approx = cv2.approxPolyDP(k, epsilon, closed=True)
            ecken = len(approx)
            Elemente.append((approx, flaeche))

            if ecken == 3:
                shape = "Dreieck"
            elif ecken == 4:
                shape = "Rechteck / Quadrat"
            else:
                shape = f"Polygon ({ecken} Ecken)"

            # print(f"{shape}, Fläche: {flaeche:.0f}px²")
            result = cv2.polylines(result, [approx], isClosed=True, color=(0, 255, 0), thickness=2)
        Konturen.put(result)
        
        groeste_flaeche = 0
        groester_approx = None
        for i in range(len(Elemente)):
            approx, flaeche = Elemente[i - 1]
            if flaeche > groeste_flaeche:
                groeste_flaeche = flaeche
                groester_approx = approx
        if groester_approx is None:
            continue
        punkte = groester_approx.reshape(-1, 2)
        mittelpunkt = np.mean(punkte, axis=0)
        print(mittelpunkt[0])