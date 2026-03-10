print("Debug: cam.py wurde geöffnet")
mode = True
import sys
import time
try:
    import libcamera
    from picamera2 import Picamera2
except ImportError:
    print("Modus von Raspberry Pi zu Laptiop gewechselt, da libcamera oder picamera2 nicht installiert ist.")
    mode = False
import cv2
import numpy as np



def run_camera(frames):
    print("Starte Kamera")

    if mode == False:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            print("Kamera konnte nicht geoeffnet werden! (VideoCapture ist nicht geöffnet)")
            return

    else:
        picam2 = Picamera2()
        picam2.start()
        print("Kamera erfolgreich gestartet")

    while True:
        if mode == False:
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

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        '''lower_blue1 = np.array([int(315 / 2), int(255 * 0.6), int(255 * 0.6)])
        upper_blue1 = np.array([int(360 / 2), 255, 255])

        lower_blue2 = np.array([0, 50, 50], dtype=np.uint8)
        upper_blue2 = np.array([200, 255, 255], dtype=np.uint8)

        mask1 = cv2.inRange(hsv, lower_blue1, upper_blue1)
        mask2 = cv2.inRange(hsv, lower_blue2, upper_blue2)
        mask = cv2.bitwise_or(mask1, mask2)
        res = cv2.bitwise_and(frame, frame, mask=mask)'''

        if frames.full():
            frames.get()  # ältesten Frame verwerfen
        frames.put(frame)