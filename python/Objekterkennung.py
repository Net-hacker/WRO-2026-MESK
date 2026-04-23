# Code zur Steuerung des Fahrt(richtung) anhand der Kamera & den Sensoren
import time
import cv2
import numpy as np
import y2
import config
# Falls man nicht auf dem Raspi runnt

def toKonturen(res_frames, Konturen, Objekte):
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
                if flaeche < 5000:
                    continue  # Rauschen ignorieren

                # Kontur annähern (epsilon = Toleranz)
                try:
                    epsilon = float(config.tolerance_values[counter]) * cv2.arcLength(k, closed=True)
                except:
                    print(type(config.tolerance_values[counter]))
                    print(type(cv2.arcLength(k, closed=True)))
                    print("Epsilon hat gekracht, setze auf Standardwert 0.2")
                    epsilon = 0.2 * cv2.arcLength(k, closed=True)
                approx = cv2.approxPolyDP(k, epsilon, closed=True)
                ecken = len(approx)
                Elemente.append((approx, flaeche, counter))
                if ecken == 3:
                    shape = "Dreieck"
                elif ecken == 4:
                    shape = "Rechteck / Quadrat"
                else:
                    shape = f"Polygon ({ecken} Ecken)"

                print(f"{shape}, Fläche: {flaeche:.0f}px²")
                if counter == 0: # Grün
                    result = cv2.polylines(result, [approx], isClosed=True, color=(0, 255, 0), thickness=2)
                elif counter == 1: # Rot
                    result = cv2.polylines(result, [approx], isClosed=True, color=(0, 0, 255), thickness=2)
                else:
                    print("Unbekannte Maske, weiße Kontur gezeichnet")
                    result = cv2.polylines(result, [approx], isClosed=True, color=(255, 255, 255), thickness=2)
            Ergebnis = cv2.bitwise_or(Ergebnis, result)
        if Konturen.full():
            Konturen.get()
        Konturen.put(Ergebnis)
        if (Objekte.full()):
            Objekte.get()
        Objekte.put(Elemente)