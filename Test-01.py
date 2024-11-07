# Dieses Programm erwartet einen Impuls auf dem GPIO15 
# Es reagiert dabei auf jeden Statuswechsel, d.h. sowohl auf eine steigende Flanke, alsauch auf eine fallende Flanke des Impulses 
# Initial wird der Signalpegel als "LOW" angenommen. Eine steigende Flanke wird dann als ein Wechsel von LOW zu HIGH definiert. 
# Ebenso ist dann definitionsgemäß eine fallende Flanke ein Wechsel von HIGH auf LOW. 
# 
# Während der HIGH Phase des Impulses wird die interne LED eingeschaltet, ansonsten bleibt sie ausgeschaltet.
#
# Wenn eine steigende Flanke erkannt wurde, dann wird die globale Variable tck1 mit einem Zeitstpempel gesetzt. 
# Eine fallende Flanke setzt dann die Variable tck2 mit einem weiteren Zeitstempel. 
# Die Differenz der beiden Zeitstempel (tck2 - tck1) ist dann die Impulsdauer. 
# 
#
# Bibliotheken laden
from machine import Pin
import utime

# Status-LED onboard
led_onboard = machine.Pin('LED', machine.Pin.OUT, value=0) 	# Definition der internen LED. 
								#  ACHTUNG!! Dieser Code gilt nur für einen Raspberry Pico W

def Signal_INT(pin):          					# Signal Interrupt Handler
    global Signal_Status      					# Signal_Status gibt den aktuellen Pegel des Impulses an
    global tck1, tck2, tck2_v, periode				# globale Variablen für die Zeitermittlung
 
    Signal.irq(handler=None)  					# Interrupt Handler abschalten während der Ausführung 
    
    if (Signal.value() == 1) and (Signal_Status == 0):  	# Signal ist jetzt aktiv (HIGH) war aber vorher auf LOW
								# Es wurde eine steigende Flanke erkannt !

        Signal_Status = 1     					# Setze Signal_Status auf HIGH
        led_onboard.value(1)    				# Schalte LED_onboard ein
        tck1 = utime.ticks_ms()					# Setze globale Variable tck1 mit einem aktuellen Zeitstempel
        print()
        print("High tck1 = ", tck1, ' ms')			# Gebe den Wert von tck1 aus
            
    elif (Signal.value() == 0) and (Signal_Status == 1): 	# Signal ist jetzt nicht aktiv (LOW) war aber vorher auf HIGH
								# Es wurde eine fallende Flanke erkant !

        Signal_Status = 0     					# Setze Signal_Status auf LOW
        led_onboard.value(0)    				# Schalte LED_onboard aus
        tck2 = utime.ticks_ms()					# Setze globale Variable tck2 mit einem aktuellen Zeitstempel
        print("Low  tck2 = ", tck2, ' ms')			# Gebe den Wert von tck2 aus
        
        ## print("tck2_v = \t", tck2_v, '\t', "tck2 = \t", tck2)
        if tck2_v > 0:						# tck2_v ist der vorherige Wert von tck2 beim letzten Aufruf
            periode = tck2 - tck2_v				#  periode gibt die Zeitdifferenz zwischen zwei fallenden Flanken an
            ## print("periode = ", periode, 'ms')
        tck2_v = tck2    					# Setze die Variable tck2_v auf den Wert von tck2 für den nächsten Aufruf
    
    Signal.irq(handler=Signal_INT)				# Interrupt Handler wieder einschalten
    

# Definiere ein "Objekt" für den Statuswechsel des Signals
Signal = machine.Pin(15,machine.Pin.IN,machine.Pin.PULL_DOWN)
# Definition des Interrupthandlers für den Statuswechsel des Signals
Signal.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=Signal_INT)



# Start des Hauptprogramms

# Setze die Status Variable für das Impulssignal
Signal_Status = Signal.value() 					# Signal_Status sollte anfänglich auf LOW gesetzt sein
								# wegen dem internen PULLDOWN Befehl auf GPIO15 
print("Signal Status: ", Signal_Status)				# Gib zur Überprüfung den initialen Zustand von Signal_Status aus


counter = 0							# Setze den Schleifenzähler initial auf 0
tck1 = 0; tck2 = 0; tck2_v = -1; periode = -1			# Setze die globalen Variablen tck2_v und periode auf ungültige Werte, 
								# da diese erst später im Signal Interrupt Handler gesetzt werden
print("Start...... !")
while True:							# Endlos Scheife
    print("counter = ", counter, "\t Pulsdauer = ", tck2-tck1, 'ms') # Gib den Schleifenzähler (couter) und die Impulsdauer aus
    utime.sleep(2)						# Warte ein wenig....
    counter += 1						# Erhöhe den Schleifenzähler
        
# Hier können weitere Aktivitäten erfolgen !!
#    
#
#######################################################################################
