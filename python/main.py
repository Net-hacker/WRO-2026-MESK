#import cv2
import keyboard
import time

from gpiozero import PWMOutputDevice, DigitalOutputDevice

# Pin-Belegung:
# 18 = LPWM (eine Richtung)
# 19 = RPWM (andere Richtung)
# 23 = L_EN
# 24 = R_EN

LPWM = PWMOutputDevice(18)       # LPWM
RPWM = PWMOutputDevice(19)       # RPWM
L_EN = DigitalOutputDevice(23)   # L_EN
R_EN = DigitalOutputDevice(24)   # R_EN

POWER = 0.7  # 20 % Leistung

Move = False
last_no_key_time = time.time()

while True:
    if not keyboard.is_pressed('w') and not keyboard.is_pressed('s'):
        if Move:  
            pass
        if time.time() - last_no_key_time > 0.05:  # 50 ms Puffer
            Move = False
    else:
        last_no_key_time = time.time()
        Move = True
    
    if Move:
        pass
    else:
        LPWM.value = 0
        RPWM.value = 0
        L_EN.off()
        R_EN.off()

    if keyboard.is_pressed('w'):
        Move = True
        # nur RPWM aktiv
        R_EN.on()
        L_EN.on()
        RPWM.value = POWER
        LPWM.value = 0
        print("VORWÄRTS")

    if keyboard.is_pressed('s'):
        Move = True
        L_EN.on()
        R_EN.on()
        LPWM.value = POWER
        RPWM.value = 0
        print("RÜCK")

    if keyboard.is_pressed("a"):
        print("LINKS")

    if keyboard.is_pressed("d"):
        print("RECHTS")

    if not keyboard.is_pressed("w") and not keyboard.is_pressed("s"):
        Move = False
        LPWM.value = 0
        RPWM.value = 0
        L_EN.off()
        R_EN.off()

    if keyboard.is_pressed("x"):
        exit()
    
    time.sleep(0.01)
'''
cam = cv2.VideoCapture(0)
while cam.isOpened():
    ret, frame = cam.read()
    if cv2.waitKey(10) == ord('q'):
        break
    cv2.imshow("WRO-CAM", frame)
'''
