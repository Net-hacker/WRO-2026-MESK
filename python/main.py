import threading
import webserver
import cam
import steuerung
from queue import Queue
import config
try:
    import libcamera
    from picamera2 import Picamera2
except ImportError:
    print("Modus von Raspberry Pi zu Laptop gewechselt, da libcamera oder picamera2 nicht installiert ist.")
    config.mode = False

frames = Queue(maxsize=5) # Neuen Queue erstellen in welchen die letzten 5 Frames gespeichert werden
res_frames = Queue(maxsize=5) # Neuen Queue erstellen in welchem die letzten 5 Maskierten Frames gespeichert werden
threading.Thread(target=webserver.host_webserver, args = (frames, res_frames)).start() # Neuen Thread für Webserver starten
threading.Thread(target=cam.run_camera, args = (frames, res_frames)).start() # Neuen Thread für Kamera starten
# threading.Thread(target=steuerung)
