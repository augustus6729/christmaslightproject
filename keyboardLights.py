#mido is the library that handles MIDI I/O
import mido
#RGB LED stuff from tutorial Dr. Allen sent me
import time
from rpi_ws281x import PixelStrip, Color
from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import urllib
import webbrowser
#import os
#Setting the backend for the file due to issues installing the default backend
mido.set_backend('mido.backends.portmidi')
#for debug purposes print backend on program start
print(mido.backend)
print(mido.get_input_names())

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
   """ parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()"""


port = mido.open_input('AKM320 MIDI 1')
print(webbrowser.get())
msg = port.receive()
#This loop constantly checks for new messages coming into the port
for msg in port.__iter__():
   #check for the correct attribute to assign an action to the msg
   #in this instance we are checking for the note attribute to assign
   #the note name to the note itself, and only on note_on msg types
    if hasattr(msg, 'note') and msg.note == 53 and msg.type == 'note_on':
        print("Call Rainbow from Flask")
        #webbrowser.open_new('http://localhost/18/on')
        #os.system("chromium-browser http://localhost/18/on")
        urllib.request.urlopen('http://localhost/18/on',data=None)
        print(msg)
    elif hasattr(msg, 'note') and msg.note == 53 and msg.type == 'note_off':
        print("Turning off")
        print("Turn Lights Off From Flask")
        urllib.request.urlopen('http://localhost/18/off',data=None)
        #os.system("chromium-browser http://localhost/18/off")
        #webbrowser.open('http://localhost/18/off',new=0,autoraise=False)
    elif hasattr(msg, 'note') and msg.note == 84 and msg.type == 'note_on':
        print(msg)
        print("White Theater Chase")
        urllib.request.urlopen('http://localhost/18/whiteTheaterChase',data=None)
    elif hasattr(msg, 'note') and msg.note == 84 and msg.type == 'note_off':
        print(msg)
        print("Clear RGB strip")
        colorWipe(strip, Color(0, 0, 0), 10)
    else:
        print(msg)
if args.clear:
    colorWipe(strip, Color(0,0,0), 10)
