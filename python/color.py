from gpiozero import DigitalOutputDevice, DigitalInputDevice
import time

# BCM Pins (unverändert übernommen)
OUT_PIN = 16
S0_PIN = 7
S1_PIN = 12
S2_PIN = 8
S3_PIN = 25

# Geräte initialisieren
s0 = DigitalOutputDevice(S0_PIN)
s1 = DigitalOutputDevice(S1_PIN)
s2 = DigitalOutputDevice(S2_PIN)
s3 = DigitalOutputDevice(S3_PIN)
out_pin = DigitalInputDevice(OUT_PIN)

# Calibration values
red_min = 40
red_max = 385
green_min = 24
green_max = 443
blue_min = 10
blue_max = 682

# Frequenzskalierung (2%)
s0.off()
s1.on()

def read_pulse_width():
    """Read the pulse width from OUT pin in microseconds"""
    
    timeout = time.time() + 0.1
    while not out_pin.value:  # LOW
        if time.time() > timeout:
            return 0
    
    pulse_start = time.time()
    timeout = time.time() + 0.1
    
    while out_pin.value:  # HIGH
        if time.time() > timeout:
            return 0
    
    pulse_end = time.time()
    return int((pulse_end - pulse_start) * 1_000_000)

def read_red():
    s2.off()
    s3.off()
    time.sleep(0.01)
    return read_pulse_width()

def read_green():
    s2.on()
    s3.on()
    time.sleep(0.01)
    return read_pulse_width()

def read_blue():
    s2.off()
    s3.on()
    time.sleep(0.01)
    return read_pulse_width()

def map_value(value, in_min, in_max, out_min, out_max):
    if in_max == in_min:
        return out_min
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def constrain(value, min_val, max_val):
    return max(min_val, min(value, max_val))

def read():
    red_readings = [read_red() for _ in range(3)]
    green_readings = [read_green() for _ in range(3)]
    blue_readings = [read_blue() for _ in range(3)]
        
    red_valid = [r for r in red_readings if r > 0]
    green_valid = [g for g in green_readings if g > 0]
    blue_valid = [b for b in blue_readings if b > 0]
        
    red_pw = sum(red_valid) // max(1, len(red_valid))
    green_pw = sum(green_valid) // max(1, len(green_valid))
    blue_pw = sum(blue_valid) // max(1, len(blue_valid))
        
    red_value = map_value(red_pw, red_min, red_max, 255, 0)
    green_value = map_value(green_pw, green_min, green_max, 255, 0)
    blue_value = map_value(blue_pw, blue_min, blue_max, 255, 0)
        
    red_value = constrain(red_value, 0, 255)
    green_value = constrain(green_value, 0, 255)
    blue_value = constrain(blue_value, 0, 255)
        
    print(f"Red = {red_value} - Green = {green_value} - Blue = {blue_value}")
        
    time.sleep(0.1)

def inter(r, g, b):
    return 1

def stop():
    s0.close()
    s1.close()
    s2.close()
    s3.close()
    out_pin.close()
