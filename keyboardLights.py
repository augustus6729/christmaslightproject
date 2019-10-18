#mido is the library that handles MIDI I/O
import mido
#RGB LED stuff from tutorial Dr. Allen sent me
import time
from rpi_ws281x import PixelStrip, Color
import asyncio
#import argparse

import RPi.GPIO as GPIO
#Setting the backend for the file due to issues installing the default backend
mido.set_backend('mido.backends.portmidi')
 
# LED strip configuration:
LED_COUNT      = 5      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

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

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel(
                (int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

# Create NeoPixel object with appropriate configuration.
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

#use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BCM)

#set channel for output
GPIO.setup(18, GPIO.OUT)

#for debug purposes print backend on program start
print(mido.backend)
print(mido.get_input_names())

# Main program logic follows:
async def main():
	port = mido.open_input('AKM320 MIDI 1')
	msg = port.receive()
#This loop constantly checks for new messages coming into the port
	for msg in port.__iter__():
#check for the correct attribute to assign an action to the msg
		if hasattr(msg, 'note') and msg.note == 53 and msg.type == 'note_on':
			await print("Turning on Orange String Lights")
			await GPIO.output(18, GPIO.HIGH)
			print(msg)
		elif hasattr(msg, 'note') and msg.note == 53 and msg.type == 'note_off':
			print("Turning off")
			GPIO.output(18, GPIO.LOW)
		elif hasattr(msg, 'note') and msg.note == 84 and msg.type == 'note_on':
			print(msg)
			print("Set RGB strip to rainbow")
			await rainbow(strip)
		elif hasattr(msg, 'note') and msg.note == 84 and msg.type == 'note_off':
			print(msg)
			await print("Clear RGB strip")
			await colorWipe(strip, Color(0, 0, 0), 10)
		else:
			print(msg)
asyncio.run(main())
#if args.clear:
#	colorWipe(strip, Color(0,0,0), 10)
# Typing Test
