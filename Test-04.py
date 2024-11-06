# In diesem Programm löst ein Signal am Eingang des GPIO15
# einen Interrupt aus. Dabei wird jede Statusänderung erfasst, d.h. 
# sowohl eine steigende als auch eine fallende Flanke bewirken
# den Aufruf der selben Interruptroutine aus (Funktion: Signal_INT()). 
# Bei einer fallende Flanke wird die aktuelle Zeit ermittelt und
# anschließend die zeitliche Differenz zu der davor aufgetretenen,
# fallenden Flanke errechnet. 
# Diese Dauer (periode) ist ein Maß für den momentanen Verbrauch.
# Je größer die Dauer, um so kleiner ist der Verbrauch. 
# Der momentane Verbrauch (mverbrauch) wird dann am Display angezeigt.
# Die interne LED blinkt kurz bei jedem Aufruf der Interruptroutine.
#
#
# Bibliotheken laden
from machine import I2C, Pin, reset
from machine_i2c_lcd import I2cLcd
from simplep import MQTTClient
import network
import utime
from _JM_priv import wlan_SSID, wlan_PW
from _JM_priv import IP_mqtt_broker, mqtt_Client, mqtt_User, mqtt_PW

# Status-LED onboard
led_onboard = machine.Pin('LED', machine.Pin.OUT, value=0)
#
# Definition of LEDs
rled 	= machine.Pin(10, machine.Pin.OUT)
yled 	= machine.Pin(11, machine.Pin.OUT)
gled 	= machine.Pin(12, machine.Pin.OUT)

# WLAN-Access und MQTT-Broker-Details
wlanSSID 	= wlan_SSID()
wlanPW 		= wlan_PW()

# MQTT-Konfiguration
mqttBroker 	= IP_mqtt_broker()
mqttClient 	= mqtt_Client()
mqttUser 	= mqtt_User()
mqttPW 		= mqtt_PW()
mqttTopic0 	= b"mpower"


def disp_lcd(z1, z2):
    # Ausgabe auf Display             
    zeile_1  = " Counter: " + str(z1) + '\n'
    zeile_2  = "Leistung: " + str(z2) + 'W \n'  
    try:
        lcd.clear()
        lcd.putstr(zeile_1)
        utime.sleep(0.2)
        lcd.putstr(zeile_2)
        utime.sleep(0.2)
    except:
        print("Z054")
    return

# Function: Connect to WLAN
def wlanConnect():
    yled.value(1); utime.sleep(2); yled.value(0)
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print('WLAN-Verbindung herstellen:', wlanSSID)
        wlan.active(True)
        wlan.connect(wlanSSID, wlanPW)
        for i in range(10):
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            led_onboard.toggle()
            print('.')
            utime.sleep(1)

    if wlan.isconnected():
            print('WLAN-Verbindung hergestellt / WLAN-Status:', wlan.status())
            ipconfig = wlan.ifconfig()
            print('IPv4-Adresse:', ipconfig[0])
            led_onboard.on()
            yled.value(1)
    else:
        print('Keine WLAN-Verbindung / WLAN-Status:', wlan.status())
        print()
        led_onboard.off()
        yled.value(0)

# Funktion: Verbindung zum MQTT Server herstellen
def mqttConnect():
    if mqttUser != '' and mqttPW != '':
        print("MQTT-Verbindung herstellen: %s mit %s als %s" % (mqttClient, mqttBroker, mqttUser))
        client = MQTTClient(mqttClient, mqttBroker, user=mqttUser, password=mqttPW, keepalive=60)
    client.connect()
    print('MQTT-Verbindung hergestellt')
    return client


def Signal_INT(pin):          # Signal Interrupt handler
    global Signal_Status      # Bezug zur globalen Variablen
    global tck1, tck2, tck2_v, periode
 
    Signal.irq(handler=None)  # Abschalten während der Ausführung 
    
    if (Signal.value() == 1) and (Signal_Status == 0):
        # Steigende Flanke 
        Signal_Status = 1     	# Setze Signal_Status auf HIGH
        led_onboard.value(1)    # Schalte LED_onboard ein
        tck1 = utime.ticks_ms() # Ermittle und speichere Zeitpunkt
        # print()
        # print("High tck1 = ", tck1, ' ms')
            
    elif (Signal.value() == 0) and (Signal_Status == 1):
        # Fallende Flanke
        Signal_Status = 0     	# Setze Signal_Status auf LOW
        led_onboard.value(0)    # Schalte LED_onboard aus
        tck2 = utime.ticks_ms() # Ermittle und speichere Zeitpunkt
        # print("Low  tck2 = ", tck2, ' ms')
        ## print("tck2_v = \t", tck2_v, '\t', "tck2 = \t", tck2)
        
        if tck2_v > 0:
            periode = tck2 - tck2_v
            # periode ist die Dauer zwischen zwei fallenden Flanken
            
        tck2_v = tck2   # speichere tck2 für den nächsten Aufruf 
    
    Signal.irq(handler=Signal_INT) # aktiviere die Interruptroutine
    

# Definiere ein "Objekt" für den Statuswechsel des Signals
Signal = machine.Pin(15,machine.Pin.IN,machine.Pin.PULL_DOWN)
# Definition des Interrupthandlers für den Statuswechsel des Signals
Signal.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=Signal_INT)


# Setze die Status Variable für das Signal
Signal_Status = Signal.value()
print("Signal Status: ", Signal_Status)

# Start des Hauptprogramms
# Initialisierung I2C
i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=100000)

# Initialisierung LCD über I2C
lcd = I2cLcd(i2c, 0x27, 2, 16)

tck1 = 0; tck2 = 0; tck2_v = -1; periode = -1
print("Start...... !")
wlanConnect()

counter = 0
while True:
    counter += 1
    rled.value(1); yled.value(0); utime.sleep(2)
    rled.value(0); yled.value(1); utime.sleep(2)    
   
    if (counter > 1) and (periode > 0):
        try:
            mverbrauch = int(3600000 / periode)
            ## print("Messung: \t", counter, "\tPeriode: \t", periode, '\t ms',"Leistung: \t", mverbrauch, '\t W')
            print("Nr: \t", counter,"\t Leistung: \t", mverbrauch, '\t W')
            rled.value(0); yled.value(0); gled.value(1); utime.sleep(0.5)
            disp_lcd(str(counter), str(mverbrauch))
            rled.value(0); yled.value(0); gled.value(0); utime.sleep(0.5)
 
 
        except:
            print("Z163")
            reset()

        myValue0 = str(mverbrauch)
        try:
            client = mqttConnect()
            client.publish(mqttTopic0, myValue0)
            print("An Topic %s gesendet: %s" %  (mqttTopic0, myValue0))
            utime.sleep(1)

            client.disconnect()
            print('MQTT-Verbindung beendet \n')

        except OSError:
            print("Z177")
            print('Fehler: Keine MQTT-Verbindung')
            print()
          
    else:
        print("Waiting... \r", end = '')
    

# Hier können weitere Aktivitäten erfolgen !!

#######################################################################################


