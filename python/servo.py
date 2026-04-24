from gpiozero import Servo
import warnings
import time
warnings.filterwarnings("ignore")  # Warnung unterdrücken

SERVO = Servo(12, min_pulse_width=1/1000, max_pulse_width=2/1000)

def steer(position: float):
    SERVO.value = max(-1.0, min(1.0, position + 0.2)) #geradestellung des servos