import board
import adafruit_bno055
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import kaliLaden

i2c = board.I2C()

sensor = adafruit_bno055.BNO055_I2C(i2c, address=0x29)

kaliLaden.load_calibration(sensor)
for i in range(10):
    matte = sensor.euler[0]
    print(f"{i}: Grad: {matte}")
    time.sleep(1)

matte = sensor.euler[0]

print(f"Grad: {matte}")

with open("../Preset/Angle.txt", "w") as file:
    file.write(f"{round(float(matte))}")
    file.close()

print("Mattenwinkel gespeichert!")
