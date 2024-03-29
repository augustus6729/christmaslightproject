import RPi.GPIO as GPIO
from flask import Flask, render_template, request
import time
from neopixel import *
import argparse
import logging
import threading

# LED strip configuration:
LED_COUNT      = 900   # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
    18 : {'name' : 'Lights', 'state' : 'off'}
    }

# Set each pin as an output and make it low:
for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   #GPIO.output(pin, GPIO.LOW)
   
class PapaBear:
    def __init__(self,start,end):
        self.start = start
        self.end = end
        self.arm1start = 0
        self.arm1end = self.end/6
        self.arm2start = self.end/6+1
        self.arm2end = self.end/3
        self.arm3start = self.end/3+1
        self.arm3end = self.end/2
        self.arm4start = self.end/2+1
        self.arm4end = self.end*2/3
        self.arm5start = self.end*2/3+1
        self.arm5end = self.end*5/6
        self.arm6start = self.end*5/6+1
        self.arm6end = self.end
        
pb = PapaBear(0,899)   
     
@app.route("/")
def main():
   # For each pin, read the pin state and store it in the pins dictionary:
   #for pin in pins:
     # pins[pin]['state'] = GPIO.input(pin)
   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'pins' : pins
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html', **templateData)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, start, end, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(start, end):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)
def colorWipe(strip, color, wait_ms=10):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        #time.sleep(wait_ms/1000.0)
    strip.show()
    
def colorWipeRange(strip, color, start, end, step, wait_ms=10):
    """Wipe color across display a pixel at a time."""
    for i in range(start,end+1, step):
        strip.setPixelColor(i, color)
        #time.sleep(wait_ms/1000.0)
    strip.show() 
def AlternatingColorWipe(strip, color, step, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(0,strip.numPixels(),step):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)
def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)
def theaterChaseRanger(strip, color,start,end, wait_ms=50, iterations=20):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(start, end, 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(start, end, 3):
                strip.setPixelColor(i+q, 0)                
def theaterChase2(strip, start, end, step,wait_ms=50):
    """attempt at red/green theater light style chaser animation."""
    for j in range(10):
        for q in range(2):
            for i in range(start, end, 2):
                strip.setPixelColor(i+q, wheel((i+j) %92))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(start, end, 2):
                strip.setPixelColor(i+q, 0)              
                    


# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = pins[changePin]['name']

   if action == "redGreenAlternate":
       colorWipeRange(strip, Color(255,0,0), pb.start, pb.end,2,10)
       colorWipeRange(strip, Color(0,255,0), pb.start+1, pb.end-1,2,10)
       message = "Alternating Red and Green"
       
   if action == "off":
     # GPIO.output(changePin, GPIO.LOW)
      message = "Turned " + deviceName + " off."
      colorWipe(strip, Color(0,0,0), 10)
      
   if action == "toggle":
      # Read the pin and set it to whatever it isn't (that is, toggle it):
      message = "Toggled " + deviceName + "."
      
   if action == "orangeRange":
       message = "Orange Range"
       colorWipeRange(strip, Color(80,255,0),0,100,1,10)
       
   if action == "candyCane":
       colorWipeRange(strip, Color(0,255,0), pb.start, pb.end,2,10)
       message = "Alternating Red and White"
       colorWipeRange(strip, Color(127,127,127), pb.start+1, pb.end-1,2,10)
       
   if action == "x":
       colorWipeRange(strip, Color(255,255,0), pb.start, pb.end,2,10)
       message = "Alternating Blue and Yellow"
       colorWipeRange(strip, Color(253,0,153), pb.start+1, pb.end-1,2,10)
   if action == "Blue":
       colorWipeRange(strip, Color(127,127,127), pb.start, pb.end,2,10)
       message = "Alternating X"
       colorWipeRange(strip, Color(0,0,255), pb.start+1, pb.end-1,2,10) 
   
   if action == "silverAndGold":
       colorWipeRange(strip,Color(255,255,255),pb.start,pb.end,2,10)
       colorWipeRange(strip,Color(255,255,47),pb.start+1,pb.end-1,2,10)
       message = "Silver and Gold"
   
   if action == "orangeSide":
      colorWipeRange(strip,Color(80,255,0),pb.start,pb.end,1,10)
      
      message = "Whole Side Orange"
   if action == "red2Blue":
      colorWipeRange(strip,Color(0,255,0),pb.arm1start,pb.arm2end,1,10)
      x=threading.Thread(target=theaterChaseRanger, args=(strip,Color(0,255,255),pb.arm3start,pb.arm4end,40,10))
      y=threading.Thread(target=theaterChaseRanger, args=(strip,Color(0,0,255),pb.arm5start,pb.end,40,10))
      x.start()
      y.start()
      message = "Red 2 Blue"
      
   if action == "pbTest":
        a=threading.Thread(target=theaterChaseRanger, args=(strip,Color(0,255,255),pb.arm1start,pb.arm1end,10,10))
        b=threading.Thread(target=theaterChaseRanger, args=(strip,Color(255,255,255),pb.arm2start,pb.arm2end,10,10))
        c=threading.Thread(target=theaterChaseRanger, args=(strip,Color(0,0,255),pb.arm3start,pb.arm3end,10,10))
        d=threading.Thread(target=theaterChaseRanger, args=(strip,Color(0,255,0),pb.arm4start,pb.arm4end,10,10))
        e=threading.Thread(target=theaterChaseRanger, args=(strip,Color(255,0,255),pb.arm5start,pb.arm5end,10,10))
        f=threading.Thread(target=theaterChaseRanger, args=(strip,Color(255,0,0),pb.arm6start,pb.arm6end,10,10))
        a.start()
        b.start()
        c.start()
        d.start()
        e.start()
        f.start()
        message = "pbTest"
        # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'message' : message,
      'pins' : pins
   }

   return render_template('main.html', **templateData)

if __name__ == "__main__":
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    app.run(host='0.0.0.0', port=80, debug=True)
