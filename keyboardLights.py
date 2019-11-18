#mido is the library that handles MIDI I/O
import mido
#RGB LED stuff from tutorial Dr. Allen sent me
import time
from rpi_ws281x import PixelStrip, Color
from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import urllib
from pygame import mixer
#import os
#Setting the backend for the file due to issues installing the default backend
mido.set_backend('mido.backends.portmidi')
#for debug purposes print backend on program start
print(mido.backend)
print(mido.get_input_names())
mixer.init()


port = mido.open_input('AKM320 MIDI 1')
msg = port.receive()
#This loop constantly checks for new messages coming into the port
for msg in port.__iter__():
   #check for the correct attribute to assign an action to the msg
   #in this instance we are checking for the note attribute to assign
   #the note name to the note itself, and only on note_on msg types
    if hasattr(msg, 'note') and msg.note == 53 and msg.type == 'note_on':
        mixer.music.load('/home/pi/christmaslightproject/TubeBells.wav')
        mixer.music.play()
        print("Call Rainbow from Flask")
        urllib.request.urlopen('http://10.200.2.129/18/on',data=None)
        print(msg)
    elif hasattr(msg, 'note') and msg.note == 84 and msg.type == 'note_on':
        print(msg)
        print("White Theater Chase")
        urllib.request.urlopen('http://10.200.2.129/18/whiteTheaterChase',data=None)
    elif hasattr(msg, 'note') and msg.note == 54 and msg.type == 'note_on':
        print(msg)
        print("Red Green Alternate")
        urllib.request.urlopen('http://10.200.2.129/18/redGreenAlternate',data=None)
    elif hasattr(msg, 'note') and msg.note == 55 and msg.type == 'note_on':
        print(msg)
        print("Color range")
        urllib.request.urlopen('http://10.200.2.129/18/redGreenAlternate',data=None)
    elif hasattr(msg, 'note') and msg.note == 83 and msg.type == 'note_on':
        print(msg)
        print("Clear colors")
        urllib.request.urlopen('http://10.200.2.129/18/off',data=None)
   
    else:
        print(msg)
if args.clear:
    colorWipe(strip, Color(0,0,0), 10)
