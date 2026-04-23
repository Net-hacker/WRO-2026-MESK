import threading
import webserver
import cam
import Objekteerkennung
from queue import Queue
import time
import config
import ultraschall as us
try:
    import libcamera
    from picamera2 import Picamera2
except ImportError:
    print("Modus von Raspberry Pi zu Laptop gewechselt, da libcamera oder picamera2 nicht installiert ist.")
    config.mode = False

config.startup() # Starte die Startup Funktion um die Presets zu laden und den Motor zu stoppen
frames = Queue(maxsize=5) # Neuen Queue erstellen in welchen die letzten 5 Frames gespeichert werden
res_frames = Queue(maxsize=5) # Neuen Queue erstellen in welchem die letzten 5 Maskierten Frames gespeichert werden
Konturen = Queue(maxsize=5)
threading.Thread(target=Objekteerkennung.toKonturen, args = (res_frames, Konturen)).start()
threading.Thread(target=webserver.host_webserver, args = (frames, Konturen)).start() # Neuen Thread für Webserver starten
threading.Thread(target=cam.run_camera, args = (frames, res_frames)).start() # Neuen Thread für Kamera starten
# threading.Thread(target=us.ultraRead).start()
