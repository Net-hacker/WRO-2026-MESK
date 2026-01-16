#import cv2
import keyboard
import RPi.GPIO as GPIO

GPIO.setup(18, GPIO.OUT) #Vorwärts
GPIO.setup(19, GPIO.OUT) #Rückwärts
GPIO.setup(23, GPIO.OUT) #Rechts
GPIO.setup(24, GPIO.OUT) #Links
Move = False

while True:
    if Move == True:
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(24, GPIO.HIGH)
    else:
        GPIO.output(23, GPIO.LOW)
        GPIO.output(24, GPIO.LOW)
        
    if keyboard.is_pressed('w'):
        Move = True
        GPIO.output(18, GPIO.HIGH)

    if keyboard.is_pressed("a"):
        print("Links")
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
