#!/usr/bin/python

# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import Adafruit_DHT
import time
import math
import get_wetterstation_march as gwm

def hum_temp_messung():
    # Sensor should be set to Adafruit_DHT.DHT11,
    # Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
    sensor = Adafruit_DHT.DHT22

    # Example using a Beaglebone Black with DHT sensor
    # connected to pin P8_11.
    pin = '5'

    # Example using a Raspberry Pi with DHT sensor
    # connected to GPIO23.
    #pin = 23
    # Try to grab a sensor reading.  Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    
    # Note that sometimes you won't get a reading and
    # the results will be null (because Linux can't
    # guarantee the timing of calls to read the sensor).
    # If this happens try again!
    if humidity is not  None and humidity <101 and temperature < 101 and temperature is not None:
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        return(round(humidity,1),round(temperature,1))
    else:
        print('Failed to get reading. Try again!')
        return(0,0)


def loop():

    i=True
    datum = str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
    while i:
        humidity, temperature= hum_temp_messung()
        fText='Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
        with open("Messwerte/log_file_"+datum+".txt","a+") as logfile:
                            text = (str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())) +" ; "+ str(temperature)+" ; "+str( humidity) +"\n")
                            logfile.write(text)
                            logfile.close()
        time.sleep(30)


def get_absolute_hum_sat(temp):
    
    #Magnus-Formel
    hum_sat= 611.2*math.exp(17.62*temp/(243.12+temp))
    hum_sat= hum_sat
    #print(("Sättigungs Wasserdampfdruck: {hum} Pa").format(hum=hum_sat))
    return(hum_sat)



def jetzt_lueften():
    # innen Messung starten
    hum, temp = hum_temp_messung()
    #print(temp)
    # Innen Feuchtigkeit berechnun
    feuchtigkeit_innen = get_absolute_hum_sat(temp) * hum * 0.01
    
    # Messwerte von der Wetterstation abrufen
    temperatur,temperatur_gefuehlt,taupunkt_temp,rel_luftfeuchte,luft_druck,boeen = gwm.get_wetterstation_data()
    # Aussen Feuchtigkeit berechnen
    feuchtigkeit_aussen= get_absolute_hum_sat(temperatur[1]) * rel_luftfeuchte[1] * 0.01
    
    delta = feuchtigkeit_innen - feuchtigkeit_aussen 
    print(("Partialdruck Wasserdampf drinnen: {delta} Pa").format(delta= str(int(feuchtigkeit_innen))))
    print(("Außentemperatur: {tempA} *C, Feuchtigkeit {humA} %").format(tempA = temperatur[1],humA =rel_luftfeuchte[1] ))
    print(("Partialdruck Wasserdampf draussen: {delta} Pa").format(delta= str(int(feuchtigkeit_aussen))))
    if delta >100:
        return(('\nDie Luft draußen ist trockener, Lüfte! \nDas Delta beträgt {delta} Pa').format(delta= str(int(delta))))
    
    elif delta >0:
        return(('\nDie Luft draußen ist ähnlich feucht wie drinnen. Lüfte, wenn du frische Luft brauchst.\nDas Delta beträgt {delta} Pa').format(delta= str(int(delta))))
        
    else: return(('\nDie Luft draußen ist feuchter als drinnen. Vermeide das Lüften.\nDas Delta beträgt {delta} Pa').format(delta= str(int(delta))))
        
    
#print(jetzt_lueften())
