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
    upper_blue = np.array([50, 255, 255])
    lower_blue = np.array([0, 10, 10])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    res = cv2.bitwise_and(frame, frame, mask=mask)

    if cv2.waitKey(10) == ord('q'):
        break
    cv2.imshow("WRO-CAM", mask)
    cv2.imshow("Test", frame)
