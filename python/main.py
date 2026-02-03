import threading
from webserver import host_webserver
import cam
from queue import Queue

frames = Queue(maxsize=5)
threading.Thread(target=host_webserver, args = (frames,)).start()
threading.Thread(target=cam.run_camera, args = (frames,)).start()