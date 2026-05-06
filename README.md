## WRO-2026-MESK

> [!Note]
> Wir haben den 3. Platz geholt und sind mit dem Projekt fertig.
> Hier wird es keine weiteren Commits geben!

Das ist das Repository auf welchem der Code für unser Roboter gelagert ist. Wir nehmen mit unserem Roboter nimmt an der WRO 2026 teil.

https://www.worldrobotolympiad.de/

https://www.worldrobotolympiad.de/saison-2026/aufgaben/future-engineers

https://www.worldrobotolympiad.de/website/docs/wro2026/WRO2026-FE-Regelwerk.pdf

https://lauschti.github.io/MESK-WRO-Doku/

## WICHTIG ZUM DEVELOPEN

Bidde, beim venv erstellen mit der Flag ``` --system-site-packages ```

## AUFRUFEN DER FUNKTIONEN (SERVO&MOTOR)

Man kann die Motor- und Servo-Funktionen wie folgt aufrufen:

Servo:
``` steer(0.0) #-1.0 (links) bis 1.0 (rechts) -> 0.0 (Mitte) ```

Motor:
``` bewegung(0.3) , -1.0 bis 1.0 für Feineinstellung ```
