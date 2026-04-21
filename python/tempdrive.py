from motor import motor, motor_stop, bewegung
from servo import steer


import time

bewegung(0.8)
steer(0.0)
print("VORWÄRTS")
time.sleep(2)

steer(1.0)

motor_stop()
print("STOP, RECHTS")


time.sleep(3)

print("LINKS")
steer(-1.0)
time.sleep(1)