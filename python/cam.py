mode = True
try:
    import libcamera
    from picamera2 import Picamera2
except ImportError:
    print("Modus von Raspberry Pi zu Laptiop gewechselt, da libcamera oder picamera2 nicht installiert ist.")
    mode = False
    import sys
import cv2
import numpy as np

def run_camera(frames):
    print("Starte Kamera")

    if mode == False:
        cam = cv2.VideoCapture(0)
        if cam == None:
            print("Kamera konnte nicht geoeffnet werden!")
            sys.exit(1)
        while cam.isOpened():
            _, frame = cam.read()
    else:
        picam2 = Picamera2()
        picam2.start()
        print("Kamera erfolgreich gestartet")

    while True:
        if mode == False:
            _, frame = cam.read()
        else:
            frame = picam2.capture_array()  # NumPy Array wie bei OpenCV

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_blue1 = np.array([int(315 / 2), int(255 * 0.6), int(255 * 0.6)])
        upper_blue1 = np.array([int(360 / 2), 255, 255])

        lower_blue2 = np.array([0, 100, 100], dtype=np.uint8)
        upper_blue2 = np.array([15, 255, 255], dtype=np.uint8)

        mask1 = cv2.inRange(hsv, lower_blue1, upper_blue1)
        mask2 = cv2.inRange(hsv, lower_blue2, upper_blue2)
        mask = cv2.bitwise_or(mask1, mask2)
        res = cv2.bitwise_and(frame, frame, mask=mask)

        if frames.full():
            frames.get()  # ältesten Frame verwerfen
        frames.put(frame)
