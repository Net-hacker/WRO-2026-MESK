import sys
import time
import cv2
import numpy as np
import config

def run_camera(frames, res_frames):
    print("Starte Kamera")

    if config.mode == False: # Wenn das Programm nicht auf dem Pi läuft
        cam = cv2.VideoCapture(0) # Starte Kamera mit cv2
        if not cam.isOpened():
            print("Kamera konnte nicht geoeffnet werden! (VideoCapture ist nicht geöffnet)")
            return
    else:
        from picamera2 import Picamera2
        picam2 = Picamera2()
        configIMG = picam2.create_still_configuration()
        picam2.configure(configIMG)
        picam2.start() # Starte Kamera mit picam2
        print("Kamera erfolgreich gestartet")

    # LoadPresets()

    while True:
        if config.mode == False: # Wenn das Programm nicht auf dem Pi läuft
            ret, frame = cam.read()
            if not ret or frame is None:
                print("Kamera liefert kein Frame, warte kurz...")
                time.sleep(0.1)
                continue
        else: # Wenn das Programm auf dem Pi läuft
            try:
                frame = picam2.capture_array()  # NumPy Array wie bei OpenCV
                if frame is None:
                    print("Picamera2: kein Frame erhalten, warte kurz...")
                    time.sleep(0.1)
                    continue
            except Exception as e: # Wenn Kamera nicht angeschlossen ist
                print("Fehler beim Erfassen mit Picamera2:", e)
                time.sleep(0.5)
                continue
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if frames.full():
            frames.get()  # ältesten Frame verwerfen
        frames.put(frame)
        generate_res(res_frames, frame)
        
def generate_res(res_frames, frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = np.zeros_like(hsv[:,:,0])

    for lower, upper in config.mask_values:
        new_mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.bitwise_or(mask, new_mask)
    
    res = cv2.bitwise_and(frame, frame, mask=mask)
    if res_frames.full():
        res_frames.get()
    res_frames.put(res)
    
def Mask_Processing(mask, hsv, number): # Braucht man nicht mehr aber ich find's ne sehr geile funktion und bin stolz drauf, deswegen lass ich sie drin
    if number < len(config.mask_values):
        new_mask = cv2.inRange(hsv, config.mask_values[number][0], config.mask_values[number][1])
        if not np.array_equal(mask, new_mask):
            print(f"UNTERSCHIED: {mask}, {new_mask}")
        return Mask_Processing(cv2.bitwise_or(mask, new_mask), hsv, number + 1)
    else:
        return mask

def load_presets():
    for x in len(config.mask_values()) - 1:
        upper, lower = load_preset(x)
    
    
    
def load_preset(id):
    if not os.path.exists("Preset/"):
        return jsonify({"sucess": False}), 404

    try:
        with open(f"Preset/{id}_Preset.txt", "r") as file:
            content = file.read()
            file.close()
    except:
        return jsonify({"sucess": False}), 404

    werte = [int(w.strip()) for w in content.split(",")]

    lower = np.array(werte[:3])
    upper = np.array(werte[3:])

    arr1 = pytojshsv(upper)
    arr2 = pytojshsv(lower)
    return arr1, arr2