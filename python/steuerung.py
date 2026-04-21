# Code zur Steuerung des Fahrt(richtung) anhand der Kamera & den Sensoren
import cv2
import numpy as np
import y2
import config
# Falls man nicht auf dem Raspi runnt
try:
    import motor
except ImportError:
    pass

def toKonturen(res_frames, Konturen):
    while True:
        results = res_frames.get()
        Ergebnis = np.zeros_like(results[0])
        counter = -1
        Elemente = []
        for result in results:
            counter = counter + 1
            grau = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

            # Konturen aus dem Bild extrahieren
            konturen, hierarchy = cv2.findContours(
                grau,
                cv2.RETR_EXTERNAL,    # nur äußere Konturen
                cv2.CHAIN_APPROX_SIMPLE  # komprimierte Darstellung
            )
            for k in konturen:
                flaeche = cv2.contourArea(k)
                if flaeche < 20000:
                    continue  # Rauschen ignorieren

                # Kontur annähern (epsilon = Toleranz)
                try:
                    epsilon = config.tolerance_values[counter] * cv2.arcLength(k, closed=True)
                except:
                    print(config.tolerance_values[counter])
                    print(cv2.arcLength(k, closed=True))
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
                if counter == 1:
                    result = cv2.polylines(result, [approx], isClosed=True, color=(0, 255, 0), thickness=2)
                elif counter == 2:
                    result = cv2.polylines(result, [approx], isClosed=True, color=(0, 0, 255), thickness=2)
                else:
                    result = cv2.polylines(result, [approx], isClosed=True, color=(255, 255, 255), thickness=2)
            Ergebnis = cv2.bitwise_or(Ergebnis, result)
        Konturen.put(Ergebnis)
        groeste_flaeche = 0
        groester_approx = None
        for approx, flaeche in Elemente:
            if flaeche > groeste_flaeche:
                groeste_flaeche = flaeche
                groester_approx = approx
        if groester_approx is None:
            continue
        punkte = groester_approx.reshape(-1, 2)
        mittelpunkt = np.mean(punkte, axis=0) # Mittelpunkt des größen Objektes bestimmen
        # print(groeste_flaeche)
        servo.steer(mittelpunkt/2500)