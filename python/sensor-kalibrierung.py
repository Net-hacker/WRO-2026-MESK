import time
import board
import adafruit_bno055
import struct

i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c, address=0x29)

print("Kalibriere den Sensor...")
print("Bewege den Sensor (Achter-Schleife), bis alle Werte auf 3 stehen.")

while True:
    # Status abfragen: Rückgabewert ist ein Tupel (sys, gyro, accel, mag)
    status = sensor.calibration_status
    sys, gyro, accel, mag = status
    
    print(f"Status: Sys={sys} Gyro={gyro} Accel={accel} Mag={mag}", end="\r")
    
    # Abbrechen, wenn alles auf 3 ist
    if sys == 3 and gyro == 3 and accel == 3 and mag == 3:
        print("\n\nVOLLSTÄNDIG KALIBRIERT!")
        break
        
    time.sleep(0.2)

# Die Daten sammeln
# Offsets sind 3x2 Bytes pro Sensor, Radien sind 1x2 Bytes
# Wir packen alles in eine Liste von 11 Integern (3+3+3+1+1)
offset_data = list(sensor.offsets_accelerometer) + \
              list(sensor.offsets_gyroscope) + \
              list(sensor.offsets_magnetometer) + \
              [sensor.radius_accelerometer, sensor.radius_magnetometer]

# 'h' steht für 'signed short' (16-bit mit Vorzeichen)
# Wir haben 11 solcher Werte
binary_data = struct.pack('<11h', *offset_data)

with open("calibration_data.bin", "wb") as f:
    f.write(binary_data)