import sys
import time
import cv2
import numpy as np
import config

def run_camera(frames, res_frames):
    print("Starte Kamera")

    if config.mode == False: # Wenn das Programm nicht auf dem Pi läuft
        cam = cv2.VideoCapture(0) # Starte Kamera mit cv2
        if not cam.isOpened():
            print("Kamera konnte nicht geoeffnet werden! (VideoCapture ist nicht geöffnet)")
            return
    else:
        from picamera2 import Picamera2
        picam2 = Picamera2()
        configIMG = picam2.create_still_configuration()
        picam2.configure(configIMG)
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
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if frames.full():
            frames.get()  # ältesten Frame verwerfen
        frames.put(frame)
        generate_res(res_frames, frame)
        
def generate_res(res_frames, frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, config.lower_blue1, config.upper_blue1)
    mask2 = cv2.inRange(hsv, config.lower_blue2, config.upper_blue2)
    mask3 = cv2.inRange(hsv, config.lower_blue3, config.upper_blue3)
    mask = cv2.bitwise_or(mask1, mask2)
    mask = cv2.bitwise_or(mask, mask3)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    if res_frames.full():
        res_frames.get()
    res_frames.put(res)