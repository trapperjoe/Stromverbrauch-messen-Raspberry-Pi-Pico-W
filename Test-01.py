# Interrupt Handling - Signal received on GPIO15

# Bibliotheken laden
from machine import Pin
import utime

# Status-LED onboard
led_onboard = machine.Pin('LED', machine.Pin.OUT, value=0)

def Signal_INT(pin):          # Signal Interrupt handler
    global Signal_Status      # Bezug zur globalen Variablen
    global tck1, tck2, tck2_v, periode
 
    Signal.irq(handler=None)  # Abschalten während der Ausführung 
    
    if (Signal.value() == 1) and (Signal_Status == 0):  # Signal ist aktiv (AN) und Signal_Status ist AUS
        Signal_Status = 1     # Setze Signal_Status auf EIN
        led_onboard.value(1)    # Schalte LED_onboard ein
        tck1 = utime.ticks_ms()
        print()
        print("High tck1 = ", tck1, ' ms')
            
    elif (Signal.value() == 0) and (Signal_Status == 1): # Signal ist nicht aktiv (AUS) und Signal_Status ist EIN
        Signal_Status = 0     # Update current Status of switch
        led_onboard.value(0)    # Setze Signal_Status auf AUS
        tck2 = utime.ticks_ms()
        print("Low  tck2 = ", tck2, ' ms')
        
        ## print("tck2_v = \t", tck2_v, '\t', "tck2 = \t", tck2)
        if tck2_v > 0:
            periode = tck2 - tck2_v
            ## print("periode = ", periode, 'ms')
        tck2_v = tck2    
    
    Signal.irq(handler=Signal_INT)
    

# Definiere ein "Objekt" für den Statuswechsel des Signals
Signal = machine.Pin(15,machine.Pin.IN,machine.Pin.PULL_DOWN)
# Definition des Interrupthandlers für den Statuswechsel des Signals
Signal.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=Signal_INT)


# Setze die Status Variable für den Signal
Signal_Status = Signal.value()
print("Signal Status: ", Signal_Status)

# Start des Hauptprogramms
counter = 0

tck1 = 0; tck2 = 0; tck2_v = -1; periode = -1
print("Start...... !")

while True:
    print("counter = ", counter, "\t Pulsdauer = ", tck2-tck1, 'ms')
    utime.sleep(2)
    counter += 1
        
    # Hier können weitere Aktivitäten erfolgen !!
    

#######################################################################################


