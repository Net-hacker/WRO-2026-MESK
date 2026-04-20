from motor import motor, motor_stop
from servo import steer


import time



motor("vor", 0.8)
steer(0.0)

time.sleep(2)


motor_stop()



time.sleep(3)