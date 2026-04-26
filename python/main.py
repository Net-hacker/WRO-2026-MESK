def main():
    import Lasersensor
    Lasersensor.Configure_I2C() # Starte den Lasersensor Scan, damit die Werte in config gespeichert werden
    import threading
    import webserver
    import cam
    import Objekterkennung
    import steuerung
    from queue import Queue
    import time
    import config
    import ultraschall as Ultra
    try:
        import libcamera
        from picamera2 import Picamera2
    except ImportError:
        print("Modus von Raspberry Pi zu Laptop gewechselt, da libcamera oder picamera2 nicht installiert ist.")
        config.mode = False

    config.startup() # Starte die Startup Funktion um die Presets zu laden und den Motor zu stoppen
    Objekte = Queue(maxsize=5)
    frames = Queue(maxsize=5) # Neuen Queue erstellen in welchen die letzten 5 Frames gespeichert werden
    res_frames = Queue(maxsize=5) # Neuen Queue erstellen in welchem die letzten 5 Maskierten Frames gespeichert werden
    Konturen = Queue(maxsize=5)
    threading.Thread(target=Ultra.checkStop).start() # Neuen Thread für die Ultraschall Stop Funktion starten
    threading.Thread(target=Lasersensor.Scan_Worker).start() # Neuen Thread für den Lasersensor Scan starten 
    threading.Thread(target=Objekterkennung.toKonturen, args = (res_frames, Konturen, Objekte)).start()
    threading.Thread(target=webserver.host_webserver, args = (frames, Konturen)).start() # Neuen Thread für Webserver starten
    threading.Thread(target=cam.run_camera, args = (frames, res_frames)).start() # Neuen Thread für Kamera starten
    threading.Thread(target=steuerung.brain, args = (Objekte,)).start()

    time.sleep(2) # Warte 2 Sekunden, damit alle Threads gestartet sind
    print(config.direction)
    # threading.Thread(target=us.ultraRead).start()

# main()