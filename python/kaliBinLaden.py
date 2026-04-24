import board
import adafruit_bno055
import struct
import time

# 1. Sensor initialisieren
i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c, address=0x29)

def load_calibration(sensor, file_path="calibration_data.bin"):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        
        # Die 11 Werte (16-bit signed shorts) wieder auspacken
        # <11h bedeutet: Little-Endian, 11 Zahlen, Typ 'short'
        vals = struct.unpack('<11h', data)
        
        # Die Werte in die Sensor-Register schreiben
        sensor.offsets_accelerometer = (vals[0], vals[1], vals[2])
        sensor.offsets_gyroscope = (vals[3], vals[4], vals[5])
        sensor.offsets_magnetometer = (vals[6], vals[7], vals[8])
        sensor.radius_accelerometer = vals[9]
        sensor.radius_magnetometer = vals[10]
        
        print("✅ Kalibrierungsdaten erfolgreich geladen!")
        return True
    except FileNotFoundError:
        print("❌ Keine Kalibrierungsdatei gefunden!")
        return False
    except Exception as e:
        print(f"❌ Fehler beim Laden: {e}")
        return False

# 2. Kalibrierung laden
load_calibration(sensor)

# 3. Kurz warten, damit der Sensor die Werte verarbeiten kann
time.sleep(0.5)

# Test-Ausgabe: Checke den Status
print(f"Aktueller Status nach Laden: {sensor.calibration_status}")