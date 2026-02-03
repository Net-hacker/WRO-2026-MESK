import cv2
import numpy as np
import sys


cam = cv2.VideoCapture(0)
if cam == None:
    print("Kamera konnte nicht geoeffnet werden!")
    sys.exit(1)

while cam.isOpened():
    _, frame = cam.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #upper_blue = np.array([50, 255, 255])
    #lower_blue = np.array([0, 10, 10])

    lower_blue1 = np.array([int(315 / 2), int(255 * 0.6), int(255 * 0.6)])
    upper_blue1 = np.array([int(360 / 2), 255, 255])

    lower_blue2 = np.array([0, 100, 100], dtype=np.uint8)
    upper_blue2 = np.array([15, 255, 255], dtype=np.uint8)

    # masken erstellen
    mask1 = cv2.inRange(hsv, lower_blue1, upper_blue1)
    mask2 = cv2.inRange(hsv, lower_blue2, upper_blue2)

    # masken kombinieren
    mask = cv2.bitwise_or(mask1, mask2)

    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imencode(".jpg", frame) # Müsste erstmal nur die Kamera sein
    if cv2.waitKey(10) == ord('q'):
        break
    cv2.imshow("WRO-CAM", mask)
    cv2.imshow("Test", frame)
