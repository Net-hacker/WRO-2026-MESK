#import cv2
import keyboard
from gpiozero import DigitalOutputDevice

Vorn = DigitalOutputDevice(18) #Vorwärts
Back = DigitalOutputDevice(19) #Rückwärts
Links = DigitalOutputDevice(23) #Links
Rechts = DigitalOutputDevice(24) #Rechts
Move = False

while True:
    if Move == True:
        Links.on()
        Rechts.on()
    else:
        GPIO.output(23, GPIO.LOW)
        GPIO.output(24, GPIO.LOW)
        
    if keyboard.is_pressed('w'):
        Move = True
        GPIO.output(18, GPIO.HIGH)

    if keyboard.is_pressed("a"):
        print("LINKS")
    if keyboard.is_pressed("s"):
        print("Rück")
    if keyboard.is_pressed("d"):
        print("Rechts")


'''cam = cv2.VideoCapture(0)
while cam.isOpened():
    ret, frame = cam.read()
    if cv2.waitKey(10) == ord('q'):
        break
    cv2.imshow("WRO-CAM", frame)'''
