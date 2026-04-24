from gpiozero import Button
import main
import time

btn = Button(10, pull_up=True)

while True:
    time.sleep(0.01)
    if btn.is_pressed:
        print("Starte Programm")
        main.main()
        break
    else:
        print("Warte auf Knopfdruck...")