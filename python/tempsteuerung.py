import keyboard
import time

from motor import motor, motor_stop
from servo import steer

servo_pos = "mitte"
Move = False
last_no_key_time = time.time()

steer(0)

power=0.7

#______________________________
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
        motor("vor", power)
        print("VORWÄRTS")

    # RÜCKWÄRTS
    if backward_pressed:
        Move = True
        motor("rueckwaerts", power)


    # LENKUNG
    if keyboard.is_pressed("a") and servo_pos != "left":
        steer(-1)
        servo_pos="left"
        print("LINKS")

    if keyboard.is_pressed("d") and servo_pos != "right":
        steer(1)
        servo_pos="right"
        print("RECHTS")

    if not keyboard.is_pressed("a") and not keyboard.is_pressed("d") and servo_pos != "mitte":
        steer(0)
        servo_pos="mitte"
        print("mitte")


    # Programm beenden
    if keyboard.is_pressed("x"):
        motor_stop()
        steer(0)
        time.sleep(1)
        break

    #CPU entlasten
    time.sleep(0.01)