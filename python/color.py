import gpiozerio as gp

OUT_PIN = 36
S0_PIN = 26
S1_PIN = 32
S2_PIN = 24
S3_PIN = 22

gp.setmode(gp.BCM)
gp.setup(S0_PIN, gp.OUT)
gp.setup(S1_PIN, gp.OUT)
gp.setup(S2_PIN, gp.OUT)
gp.setup(S3_PIN, gp.OUT)
gp.setup(OUT_PIN, gp.IN)

gp.output(S0_PIN, gp.LOW)
gp.output(S1_PIN, gp.HIGH)

red_min = 999999
red_max = 0
green_min = 999999
green_max = 0
blue_min = 999999
blue_max = 0

def read_pulse_width():
    timeout = time.time() + 0.1
    while gp.input(OUT_PIN) == gp.LOW:
        if time.time() > timeout:
            return 0

    pulse_start = time.time()
    timeout = time.time() + 0.1
    while gp.input(OUT_PIN) == gp.HIGH:
        if time.time() > timeout:
            return 0
    pulse_end = time.time()

    return int((pulse_end - pulse_start) * 1000000)

def read_red():
    gp.output(S2_PIN, gp.LOW)
    gp.output(S3_PIN, gp.LOW)
    time.sleep(0.01)
    return read_pulse_width()

def read_green():
    gp.output(S2_PIN, gp.HIGH)
    gp.output(S3_PIN, gp.HIGH)
    time.sleep(0.01)
    return read_pulse_width()

def read_blue():
    gp.output(S2_PIN, gp.LOW)
    gp.output(S3_PIN, gp.HIGH)
    time.sleep(0.01)
    return read_pulse_width()

try:
    while True:
        red_reading = [read_red() for _ in range(3)]
        green_reading = [read_green() for _ in range(3)]
        blue_reading = [read_blue() for _ in range(3)]

        red_pw = sum(r for r in red_reading if r > 0) // max(1, len([r for r in red_reading if r > 0]))
        green_pw = sum(g for g in green_reading if g > 0) // max(1, len([g for g in green_reading if g > 0]))
        blue_pw = sum(b for b in blue_reading if b > 0) // max(1, len([b for b in blue_reading if b > 0]))

        if red_pw > 0 and red_pw < red_min:
            red_min = red_pw
        if green_pw > 0 and green_pw < green_min:
            green_min = green_pw
        if blue_pw > 0 and blue_pw < blue_min:
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
    print(f"\nFinale Kalibrierungswerte:")
    print(f"redMin = {red_min}, redMax = {red_max}")
    print(f"greenMin = {green_min}, greenMax = {green_max}")
    print(f"blueMin = {blue_min}, blueMax = {blue_max}")

finally:
    gp.cleanup()
