# Sensoransteuerung für Smart Glove

Diese Applikation bietet eine Schnittstelle zu den verbauten Sensoren
des Smart Gloves.

Das Transportprotokoll ist in GloveControl/GloveControl.ino definiert.

Kommunikation: Arduino LilyPad -> PC über serielle Schnittstelle.


Angeschlossene Sensoren:
* 4 "Berührungssensoren" (einen pro Finger)
* Accelerometer
* (Die Flexsensoren an den Fingern sind noch nicht angeschlossen)

Datenübertragungsrate: 10 Packete pro Sekunde (bzw. 100 ms delay zwischen den Übertragungen).

Die Übertragung erfolgt asynchron über callback Methoden. 

## Benötigte python packages

* pyserial 
 
## Beispiel
Die main.py bietet ein Beispiel zur Benutzung des Moduls.