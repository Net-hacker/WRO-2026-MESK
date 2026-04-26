import servo

while True:
    value = input("Geben Sie den Servo-Wert ein (-1.0 bis 1.0): ")
    try:
        position = float(value)
        if -1.0 <= position <= 1.0:
            servo.steer(position)
            print(f"Servo auf Position {position} eingestellt.")
        else:
            print("Bitte geben Sie einen Wert zwischen -1.0 und 1.0 ein.")
    except ValueError:
        print("Ungültige Eingabe. Bitte geben Sie eine Zahl zwischen -1.0 und 1.0 ein.")