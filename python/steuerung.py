import keyboard
import time

from gpiozero import PWMOutputDevice, DigitalOutputDevice

#______________________________________________________________________________________
# Pin-Belegung (BCM):
# 18 = LPWM (eine Richtung)
# 19 = RPWM (andere Richtung)
# 23 = L_EN
# 24 = R_EN
# 12 = Servo
#_______________________________________________________________________________________

#Motor Setup____________________________________________________________________________
LPWM = PWMOutputDevice(18)
RPWM = PWMOutputDevice(19)
L_EN = DigitalOutputDevice(23)
R_EN = DigitalOutputDevice(24)
POWER = 0.3  

#Servo Setup____________________________________________________________________________
SERVO = PWMOutputDevice(12, frequency=65)
SERVO_LEFT   = 0.047  
SERVO_CENTER = 0.075  
SERVO_RIGHT  = 0.1 
servo_pos = "mitte"


Move = False
last_no_key_time = time.time()


def motor_stop():
    global Move
    Move = False
    LPWM.value = 0
    RPWM.value = 0
    L_EN.off()
    R_EN.off()

def servo_set(pos):
        SERVO.value = pos

servo_set(SERVO_CENTER)

#________________________________________________________________________________________
while True:
    forward_pressed  = keyboard.is_pressed('w')
    backward_pressed = keyboard.is_pressed('s')

    # Puffer, bevor Motor stoppt
    if not forward_pressed and not backward_pressed:
        if time.time() - last_no_key_time > 0.05:  # 50 ms Puffer
            motor_stop()
    else:
        last_no_key_time = time.time()
        Move = True
    if not Move:
        motor_stop()


    # VORWÄRTS
    if forward_pressed:
        Move = True
        L_EN.on()
        R_EN.on()
        RPWM.value = POWER
        LPWM.value = 0
        print("VORWÄRTS")

    # RÜCKWÄRTS
    if backward_pressed:
        Move = True
        L_EN.on()
        R_EN.on()
        LPWM.value = POWER
        RPWM.value = 0
        print("RÜCK")


    # LENKUNG (this is a test)
    if keyboard.is_pressed("a") and servo_pos != "left":
        servo_set(SERVO_LEFT)
        servo_pos="left"
        print("LINKS")

    if keyboard.is_pressed("d") and servo_pos != "right":
        servo_set(SERVO_RIGHT)
        servo_pos="right"
        print("RECHTS")

    if not keyboard.is_pressed("a") and not keyboard.is_pressed("d") and servo_pos != "mitte":
        servo_set(SERVO_CENTER)
        servo_pos="mitte"
        print("mitte")


    # Programm beenden
    if keyboard.is_pressed("x"):
        motor_stop()
        SERVO.value = 0
        break

    #CPU entlasten
    time.sleep(0.01)