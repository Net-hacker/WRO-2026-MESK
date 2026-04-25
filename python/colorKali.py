from gpiozero import DigitalOutputDevice, DigitalInputDevice
import time


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

# Frequenzskalierung setzen
s0.off()
s1.on()

red_min = 999999
red_max = 0
green_min = 999999
green_max = 0
blue_min = 999999
blue_max = 0

def read_pulse_width():
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

try:
    while True:
        red_reading = [read_red() for _ in range(3)]
        green_reading = [read_green() for _ in range(3)]
        blue_reading = [read_blue() for _ in range(3)]

        red_valid = [r for r in red_reading if r > 0]
        green_valid = [g for g in green_reading if g > 0]
        blue_valid = [b for b in blue_reading if b > 0]

        red_pw = sum(red_valid) // max(1, len(red_valid))
        green_pw = sum(green_valid) // max(1, len(green_valid))
        blue_pw = sum(blue_valid) // max(1, len(blue_valid))

        if 0 < red_pw < red_min:
            red_min = red_pw
        if 0 < green_pw < green_min:
            green_min = green_pw
        if 0 < blue_pw < blue_min:
            blue_min = blue_pw

        if red_pw > red_max:
            red_max = red_pw
        if green_pw > green_max:
            green_max = green_pw
        if blue_pw > blue_max:
            blue_max = blue_pw

        print("-" * 42)
        print(f"Red PW = {red_pw} - Green PW = {green_pw} - Blue PW = {blue_pw}")
        print(f"  Min -> R:{red_min} G:{green_min} B:{blue_min}")
        print(f"  Max -> R:{red_max} G:{green_max} B:{blue_max}")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nKalibrierung gestoppt")
    print(f"redMin = {red_min}, redMax = {red_max}")
    print(f"greenMin = {green_min}, greenMax = {green_max}")
    print(f"blueMin = {blue_min}, blueMax = {blue_max}")

finally:
    # gpiozero räumt automatisch auf, aber explizit geht auch:
    s0.close()
    s1.close()
    s2.close()
    s3.close()
    out_pin.close()
