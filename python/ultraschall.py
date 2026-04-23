from gpiozero import DistanceSensor

sLinks = DistanceSensor(echo=21, trigger=20)
sRechts = DistanceSensor(echo=26, trigger=16)



def ultraRead():
    while True:
        distL = sLinks.distance * 100
        distR = sRechts.distance * 100
        if distL == 100:
            continue
        #else:
            #print("Ultra Links: ", distL)
        if distR == 100:
            continue
        #else:
            #print("Ultra Rechts", distR)
        print("Ultra Rechts: ", distR, "  Ultra Links: ", distL)