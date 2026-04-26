#from gpiozero import Servo
#import warnings
#import time
#warnings.filterwarnings("ignore")  # Warnung unterdrücken

#SERVO = Servo(12, min_pulse_width=1/1000, max_pulse_width=2/1000)

#def steer(position: float):
#    SERVO.value = max(-1.0, min(1.0, position + 0.2)) #geradestellung des servos

import warnings
import time
warnings.filterwarnings("ignore")

PWM_PATH = "/sys/class/pwm/pwmchip0/pwm0"

# Einmalig initialisieren
def init_servo():
    # Export falls noch nicht geschehen
    try:
        with open("/sys/class/pwm/pwmchip0/export", "w") as f:
            f.write("0")
    except OSError:
        pass  # Bereits exportiert, ignorieren
    
    time.sleep(0.1)  # Kurz warten bis pwm0 erscheint
    
    with open(f"{PWM_PATH}/period", "w") as f:
        f.write("20000000")
    with open(f"{PWM_PATH}/enable", "w") as f:
        f.write("1")

def steer(position: float):
    position = max(-1.0, min(1.0, position + 0.2))  # dein Offset
    pulse_us = int(1500 + position * 500)  # -1..1 → 1000..2000µs
    with open(f"{PWM_PATH}/duty_cycle", "w") as f:
        f.write(str(pulse_us * 1000))  # µs → ns

init_servo()