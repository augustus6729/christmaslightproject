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
   
class Tree:
    def __init__(self,start,end):
        self.start = start
        self.end = end
class Bush:
    def __init__(self,start,end):
        self.start = start
        self.end = end

t1 = Tree(0,299)
t2 = Tree(600,899)
b1 = Bush(300,449)
b2 = Bush(450,599)

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
            for i in range(0, strip.numPixels(), 2):
                strip.setPixelColor(i+q, wheel((i+j) %92))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 2):
                strip.setPixelColor(i+q, 0)              
def theaterChase3(strip, tc3start, tc3end, step,wait_ms=50):
    """attempt at red/green theater light style chaser animation."""
    for j in range(10):
        for q in range(2):
            for i in range(tc3start, tc3end, 2):
                strip.setPixelColor(i+q, wheel((i+j) %154))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(tc3start, tc3end, 2):
                strip.setPixelColor(i+q, 0)                   

threads = list() 
                          
# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = pins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
      x=threading.Thread(target=rainbow, args=(strip,t1.start,t1.end,1,1))
      x.start()
      y=threading.Thread(target=rainbow, args=(strip,t2.start,t2.end,1,1))
      y.start()
      # Rainbow Trees
      # Save the status message to be passed into the template:
      message = "Turned " + deviceName + " on."
  
   if action == "whiteTheaterChase":
       x=threading.Thread(target=theaterChaseRanger, args=(strip, Color(127,127,127), t1.start, t1.end,40,10))
       y=threading.Thread(target=theaterChaseRanger, args=(strip, Color(127,127,127), b1.start, b1.end,40,10))
       x.start()
       y.start()
       message = "White Theater Chase."
   if action == "americaTree":
       colorWipeRange(strip,Color(0,255,0),t1.start,t1.end,3,10)
       colorWipeRange(strip,Color(127,127,127),t1.start+1,t1.end-1,3,10)
       colorWipeRange(strip,Color(0,0,255),t1.start+2,t1.end-2,3,10)
       colorWipeRange(strip,Color(0,255,0),t2.start,t2.end,3,10)
       colorWipeRange(strip,Color(127,127,127),t2.start+1,t2.end-1,3,10)
       colorWipeRange(strip,Color(0,0,255),t2.start+2,t2.end-2,3,10)
       message = "America Tree"  
       #theaterChaseRainbow(strip)  
   if action == "americaBear":
       colorWipeRange(strip,Color(0,255,0),t1.start,t1.end,3,10)
       colorWipeRange(strip,Color(127,127,127),t1.start+1,t1.end-1,3,10)
       colorWipeRange(strip,Color(0,0,255),t1.start+2,t1.end-2,3,10)
       colorWipeRange(strip,Color(0,255,0),b1.start,b1.end,3,10)
       colorWipeRange(strip,Color(127,127,127),b1.start+1,b1.end-1,3,10)
       colorWipeRange(strip,Color(0,0,255),b1.start+2,b1.end-2,3,10)
       colorWipeRange(strip,Color(0,255,0),t2.start,t2.end,3,10)
       colorWipeRange(strip,Color(127,127,127),t2.start+1,t2.end-1,3,10)
       colorWipeRange(strip,Color(0,0,255),t2.start+2,t2.end-2,3,10)
       message = "America Tree"
   if action == "americaBush":
       colorWipeRange(strip,Color(0,255,0),b1.start,b1.end,3,10)
       colorWipeRange(strip,Color(127,127,127),b1.start+1,b1.end-1,3,10)
       colorWipeRange(strip,Color(0,0,255),b1.start+2,b1.end-2,3,10)
       message = "AMERICA bush"
   if action == "3colorBush":
       colorWipeRange(strip,Color(0,255,255),b1.start,b1.end,3,10)
       colorWipeRange(strip,Color(255,255,47),b1.start+1,b1.end-1,3,10)
       colorWipeRange(strip,Color(127,127,127),b1.start+2,b1.end-2,3,10)
       message = "gold silver purple"
   if action == "ccBush":
       colorWipeRange(strip,Color(0,255,0),b1.start,b1.end,2,10)
       colorWipeRange(strip,Color(127,127,127),b1.start+1,b1.end-2,2,10)
       message="candy cane bush"
   if action == "bushBlue":
       x=threading.Thread(target=theaterChaseRanger, args=(strip, Color(0,0,255), b1.start, b1.end,40,10))
       x.start()
       message = "Bush Blue"
   if action == "5colorBush":
       colorWipeRange(strip,Color(0,255,255),b1.start,b1.end,5,10)
       colorWipeRange(strip,Color(0,255,0),b1.start+1,b1.end-1,5,10)
       colorWipeRange(strip,Color(127,127,127),b1.start+2,b1.end-2,5,10)
       colorWipeRange(strip,Color(255,255,47),b1.start+3,b1.end-3,5,10)
       colorWipeRange(strip,Color(255,0,0),b1.start+4,b1.end-4,5,10)
       message = "gold silver purple"    
   if action == "4colorTree":
       colorWipeRange(strip,Color(255,255,47),t1.start,t1.end,4,10)
       colorWipeRange(strip,Color(0,255,0),t1.start+1,t1.end-1,4,10)
       colorWipeRange(strip,Color(127,127,100),t1.start+2,t1.end-2,4,10)
       colorWipeRange(strip,Color(255,0,0),t1.start+3,t1.end-3,4,10)
       colorWipeRange(strip,Color(255,255,47),t2.start,t2.end,4,10)
       colorWipeRange(strip,Color(0,255,0),t2.start+1,t2.end-1,4,10)
       colorWipeRange(strip,Color(127,127,100),t2.start+2,t2.end-2,4,10)
       colorWipeRange(strip,Color(255,0,0),t2.start+3,t2.end-3,4,10)
       message = "4color tree"
   if action == "treeBlue":
       x=threading.Thread(target=theaterChaseRanger, args=(strip, Color(0,0,255), t1.start, t1.end,40,10))
       y=threading.Thread(target=theaterChaseRanger, args=(strip, Color(255,255,47), t2.start, t2.end,40,10))
       x.start()
       y.start()
       message = "Blue and gold."
   if action == "redGreenAlternate":
       x=threading.Thread(target=colorWipeRange, args=(strip, Color(255,0,0), t1.start, t2.end,2,10))
       y=threading.Thread(target=colorWipeRange, args=(strip, Color(0,255,0), t1.start+1, t2.end,2,10))
       x.start()
       y.start()
       # move to papabear
       #colorWipeRange(strip, Color(255,0,0), 0, strip.numPixels(),2,10)
       #colorWipeRange(strip, Color(0,255,0), 1, strip.numPixels()-1,2,10)
       message = "Alternating Red and Green"
   if action == "ccTheaterChase":
       x=threading.Thread(target=theaterChaseRanger, args=(strip, Color(127,127,127), b1.start, b1.end,40,10))
       #y=threading.Thread(target=theaterChaseRanger, args=(strip, Color(0,255,0), b2.start, b2.end,40,10))
       x.start()
       #.start()
       #Put y lines on other bush (knew start and end)
       #theaterChase(strip, Color(127, 127, 127,))
       #theaterChase(strip, Color(0, 255, 0))
       message = "candycaneTheater Chase."
   if action == "whiteTheaterChase":
       x=threading.Thread(target=theaterChaseRanger, args=(strip, Color(127,127,127), b1.start, b1.end,40,10))
       
       x.start()
       
       message = "White Theater Chase."
   if action == "theaterChaseRanger":
      
       x=threading.Thread(target=theaterChaseRanger, args=(strip, Color(204,204,0), b1.start, b1.end,40,10))
       #y=threading.Thread(target=theaterChaseRanger, args=(strip, Color(0,127,255), b2.start, b2.end,40,10)) 
       x.start()
       #y.start()
       #Put y lines on other bush (knew start and end)
      
       message = "multi" 
   if action == "theaterChase2":
       x=threading.Thread(target=theaterChase2, args=(strip,b1.start,b1.end,2,50))
       x.start()
       message = "multi"
   if action == "theaterChase3":
       x=threading.Thread(target=theaterChase3, args=(strip,b1.start,b1.end,2,50))
       x.start()
       message = "multi"
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
       colorWipeRange(strip, Color(0,255,0), 0, strip.numPixels(),2,10)
       message = "Alternating Red and White"
       colorWipeRange(strip, Color(127,127,127), 1, strip.numPixels()-1,2,10)
   if action == "x":
       colorWipeRange(strip, Color(255,255,0), 0, strip.numPixels(),2,10)
       message = "Alternating Blue and Yellow"
       colorWipeRange(strip, Color(253,0,153), 1, strip.numPixels()-1,2,10)
   if action == "Blue":
      # move to papabear
       colorWipeRange(strip, Color(127,127,127), 0, strip.numPixels(),2,10)
       message = "Alternating X"
       colorWipeRange(strip, Color(0,0,255), 1, strip.numPixels()-1,2,10) 
   if action == "purpleTheaterChase":
       x=threading.Thread(target=theaterChaseRanger, args=(strip, Color(0,204,255), t1.start, t1.end,40,10))
       y=threading.Thread(target=theaterChaseRanger, args=(strip, Color(0,204,255), t2.start, t2.end,40,10))
       x.start()
       y.start()
       #theaterChase(strip, Color(0,204,255))
       message = "purple Theater Chase."
   
   if action == "coralAndGreen":
       colorWipeRange(strip,Color(85,255,85),0,strip.numPixels(),2,10)
       colorWipeRange(strip,Color(255,0,0),1,strip.numPixels()-1,2,10)
       message = "Coral and Green"
   if action == "silverAndGold":
       colorWipeRange(strip,Color(255,255,255),0,strip.numPixels(),2,10)
       colorWipeRange(strip,Color(255,255,47),1,strip.numPixels()-1,2,10)
       message = "Silver and Gold"
   if action == "treeTest":
       colorWipeRange(strip,Color(255,255,255),t1.start,t1.end/4,1,10)
       colorWipeRange(strip,Color(0,255,0),t1.end/4+1,t1.end/2,1,10)
       colorWipeRange(strip,Color(255,255,0),t1.end/2+1,t1.end*3/4,1,10)
       colorWipeRange(strip,Color(255,0,255),t1.end*3/4+1,t1.end,1,10)
       colorWipeRange(strip,Color(255,255,255),t2.start,t2.end/4+450,1,10)
       colorWipeRange(strip,Color(0,255,0),t1.end/4+451,t1.end/2+450,1,10)
       colorWipeRange(strip,Color(255,255,0),t1.end/2+451,t1.end*3/4+450,1,10)
       colorWipeRange(strip,Color(255,0,255),t1.end*3/4+451,t1.end+450,1,10)
       message = "Tree Test"
   if action == "bushTest":
        colorWipeRange(strip,Color(255,0,0),300,324,1,10)
        colorWipeRange(strip,Color(0,255,0),325,349,1,10)
        colorWipeRange(strip,Color(0,0,255),350,374,1,10)
        colorWipeRange(strip,Color(255,255,0),375,399,1,10)
        colorWipeRange(strip,Color(0,0,255),400,424,1,10)
        colorWipeRange(strip,Color(255,0,255),425,449,1,10)
        #colorWipeRange(strip,Color(255,0,0),b1.start,t1.end/6+300,1,10)
        #colorWipeRange(strip,Color(0,255,0),t1.end/6+301,t1.end/3+200,1,10)
        #colorWipeRange(strip,Color(0,0,255),t1.end/3+201,t1.end/2,1,10)
        #colorWipeRange(strip,Color(255,0,255),t1.end/2+1,t1.end*2/3,1,10)
        #colorWipeRange(strip,Color(0,255,255),t1.end*2/3+1,t1.end*5/6,1,10)
        message = "Bush Test"
   if action == "whiteBushChase":
      x=threading.Thread(target=theaterChaseRanger, args=(strip, Color(204,204,204), b1.start, b1.end,40,10))
      #theaterChaseRanger(strip,Color(204,204,204),b1.start,b1.end,40,10) 
      x.start()
      message = "Bush Chase"
   if action == "bushGreenGold":
      colorWipeRange(strip,Color(255,0,0),b1.start,b1.end,2,10)
      colorWipeRange(strip,Color(255,255,0),b1.start+1,b1.end-1,2,10)
      message = "Bush 1 Green and Gold"
   if action == "bushPink":
      colorWipeRange(strip,Color(55,190,51),b1.start,b1.end,1,10)
      message = "Pink Bushes"
   if action == "pinkRedWhite":
       colorWipeRange(strip,Color(55,190,51),b1.start,b1.end,3,10)
       colorWipeRange(strip,Color(0,255,0),b1.start+1,b1.end-1,3,10)
       colorWipeRange(strip,Color(127,127,127),b1.start+2,b1.end-2,3,10)
       message="pinkredwhiteBUSH"
   if action == "treeComboChase":
      x=threading.Thread(target=theaterChaseRanger, args=(strip,Color(0,255,0),t1.start,t1.end,40,10))
      y=threading.Thread(target=theaterChaseRanger, args=(strip,Color(255,255,255),t2.start,t2.end,40,10))
      x.start()
      y.start()
      message = "Combo Chase Candy Cane"
   if action == "babyColors":
      colorWipeRange(strip,Color(202,247,201),t1.start,t1.end,1,10)
      colorWipeRange(strip,Color(168,146,255),t2.start,t2.end,1,10)
      message = "Baby Blue and Pastel Pink"
   if action == "orangeSide":
      colorWipeRange(strip,Color(80,255,0),t1.start,t1.end,1,10)
      colorWipeRange(strip,Color(80,255,0),b1.start,b1.end,1,10)
      colorWipeRange(strip,Color(80,255,0),t2.start,t2.end,1,10)
      message = "Whole Side Orange"
   if action == "red2Blue":
      colorWipeRange(strip,Color(0,255,0),t1.start,t1.end,1,10)
      x=threading.Thread(target=theaterChaseRanger, args=(strip,Color(0,255,255),b1.start,b1.end,40,10))
      y=threading.Thread(target=theaterChaseRanger, args=(strip,Color(0,0,255),t2.start,t2.end,40,10))
      x.start()
      y.start()
      message = "Red 2 Blue"
   if action == "christmasTrees":
      colorWipeRange(strip,Color(205,255,47),t1.start,t1.end,5,10)
      colorWipeRange(strip,Color(205,255,47),t2.start,t2.end,5,10)
      message = "Crhistmas Tree Lighting"
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
