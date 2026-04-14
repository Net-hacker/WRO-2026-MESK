## WRO-2026-MESK

Das ist das Repository auf welchem der Code für unser Roboter gelagert ist. Wir nehmen mit unserem Roboter nimmt an der WRO 2026 teil.

https://www.worldrobotolympiad.de/

https://www.worldrobotolympiad.de/saison-2026/aufgaben/future-engineers

https://www.worldrobotolympiad.de/website/docs/wro2026/WRO2026-FE-Regelwerk.pdf

https://lauschti.github.io/MESK-WRO-Doku/


## Raspberry-Pi

Username: wro-user
Password: WRO123!

Tailscale IP:
100.86.245.113

## WICHTIG ZUM DEVELOPEN

Bidde, beim venv erstellen mit der Flag ``` --system-site-packages ```

Vor installieren der Packages: ``` pip install --upgrade matplotlib pandas-stubs Flask-SQLAlchemy ```

## AUFRUFEN DER FUNKTIONEN (SERVO&MOTOR)

Man kann die Motor- und Servo-Funktionen wiefolgt aufrufen:

Servo:
``` steer(0.0) #-1.0 (rechts) bis 1.0 (links) -> 0.0 (Mitte) ```

Motor: 
``` motor(vorwaerts, 0.3) #vorwaerts/rueckwaerts, 0.0 bis 1.0 für feineinstellung ```
