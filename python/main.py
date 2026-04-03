import threading
from webserver import host_webserver
import cam
from queue import Queue
import config
try:
    import libcamera
    from picamera2 import Picamera2
except ImportError:
    print("Modus von Raspberry Pi zu Laptiop gewechselt, da libcamera oder picamera2 nicht installiert ist.")
    config.mode = False

frames = Queue(maxsize=5)
threading.Thread(target=host_webserver, args = (frames,)).start()
threading.Thread(target=cam.run_camera, args = (frames,)).start()