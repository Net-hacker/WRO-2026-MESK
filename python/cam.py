import sys
import time
import cv2
import numpy as np
import config


def run_camera(frames):
    print("Starte Kamera")

    if config.mode == False: # Wenn das Programm nicht auf dem Pi läuft
        cam = cv2.VideoCapture(0) # Starte Kamera mit cv2
        if not cam.isOpened():
            print("Kamera konnte nicht geoeffnet werden! (VideoCapture ist nicht geöffnet)")
            return
    else: # Wenn das Programm auf dem Pi läuft
        picam2 = Picamera2()
        picam2.start() # Starte Kamera mit picam2
        print("Kamera erfolgreich gestartet")

    while True:
        if config.mode == False: # Wenn das Programm nicht auf dem Pi läuft
            ret, frame = cam.read()
            if not ret or frame is None:
                print("Kamera liefert kein Frame, warte kurz...")
                time.sleep(0.1)
                continue
        else: # Wenn das Programm auf dem Pi läuft
            try:
                frame = picam2.capture_array()  # NumPy Array wie bei OpenCV
                if frame is None:
                    print("Picamera2: kein Frame erhalten, warte kurz...")
                    time.sleep(0.1)
                    continue
            except Exception as e: # Wenn Kamera nicht angeschlossen ist
                print("Fehler beim Erfassen mit Picamera2:", e)
                time.sleep(0.5)
                continue

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Variable hsv wird auf Daten der Kamera gesetzt

        if frames.full():
            frames.get()  # ältesten Frame verwerfen
        frames.put(frame)