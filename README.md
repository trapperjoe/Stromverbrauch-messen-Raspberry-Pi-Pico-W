Vor kurzem stand ich vor folgender Problemstellung: 
Mein Stromverbrauch ist (gefühlt) zu hoch und ich wollte der Sache auf den Grund gehen und "Stromfresser" finden und eliminieren. 

Dazu wollte ich meinen atuellen Stromverbrauch einfach ablesen aber mein Stromverbrauchszähler im Keller ist schon älter und sendet nur Lichtimpulse und zwar umso 
schneller, je mehr Strom fließt.  Leider ist mein Stromverbrauchszähler nicht "smart", so dass es keine Möglichkeit gibt, dass er weitere Messdaten liefern 
oder anzeigen kann, weder optisch noch elektrisch. Man kann lediglich die Zählerdaten ablesen, nicht aber den momentanen "Verbrauch". 

Was tun ?
Natürlich kann man mit  einer Stoppuhr daneben stehen und die Zeitdauer zwischen zwei Impulsen messen. Diese dann aufschreiben und später ausrechnen, welcher momentanen  
Leistung dies entspricht. Das ist aber kein flexibles Verfahren, zudem sehr ungenau. 

Eine bessere Lösung ist es mit einer kleinen elektronischen Schaltung die Dauer zwischen zwei Impulsen zu messen, diese in einen momentanen Leistungswert umzurechnen und 
dann anzuzeigen. 

Auf meinem Stromverauchszähler steht, dass er pro kWh 1000 Impulse liefert. 
Beispiel:
Bei einer (angenommenen) Periode von 10 Sekunden zwischen zwei benachbarten Impulsen sind das 6 Impulse pro Minute und damit 360 Impulse pro Stunde. 
Das entspricht also einer momentanen Leistung von 360 Watt. 
Bei einer (angenommenen) Periode von 1 Sekunde zwischen zwei benachbarten Impulsen sind das 60 Impulse pro Minute und damit 3600 Impulse pro Stunde. 
Das entspricht also einer momentanen Leistung von 3600 Watt. 

Die Zeitmessung auf dem Raspberry Pi Pico W sollte sinnvollerweise in Millisekunden erfolgen. 
Daher lautet die Formel für die Umrechnung. 

Pm = 3600000 / Tp 

wobei Pm die momentane Leistung in Watt ist und Tp die Periodendauer in Millisekunden zwischen zwei benachbarten Impulsen.

Bei der hier vorgestellten Lösung lösen die Lichtimpulse jeweils einen Interrupt aus. 
Die Berechnung der Momentanleistung und die Anzeige bzw. Weiterleitung an den MQTT-Broker geschieht dann im Hauptprogramm. 

