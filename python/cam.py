print("Debug: cam.py wurde geöffnet")
import sys
import time
import cv2
import numpy as np
import config


def run_camera(frames):
    print("Starte Kamera")

    if config.mode == False:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            print("Kamera konnte nicht geoeffnet werden! (VideoCapture ist nicht geöffnet)")
            return
    else:
        from picamera2 import Picamera2
        picam2 = Picamera2()
        picam2.start()
        print("Kamera erfolgreich gestartet")

    while True:
        if config.mode == False:
            ret, frame = cam.read()
            if not ret or frame is None:
                print("Kamera liefert kein Frame, warte kurz...")
                time.sleep(0.1)
                continue
        else:
            try:
                frame = picam2.capture_array()  # NumPy Array wie bei OpenCV
                if frame is None:
                    print("Picamera2: kein Frame erhalten, warte kurz...")
                    time.sleep(0.1)
                    continue
            except Exception as e:
                print("Fehler beim Erfassen mit Picamera2:", e)
                time.sleep(0.5)
                continue

        if frames.full():
            frames.get()  # ältesten Frame verwerfen
        frames.put(frame)
