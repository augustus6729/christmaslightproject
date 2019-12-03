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
mixer.pre_init(44100, -16, 2, 1024)
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
        urllib.request.urlopen('http://10.200.2.137/18/on',data=None)
        print(msg)
    if hasattr(msg, 'note') and msg.note == 53 and msg.type == 'note_off':
        mixer.music.stop()
    
    if hasattr(msg, 'note') and msg.note == 54 and msg.type == 'note_on':
        mixer.music.load('./fluteF6.wav')
        mixer.music.play()
        print(msg)
        print("Red Green Alternate")
        urllib.request.urlopen('http://10.200.2.137/18/redGreenAlternate',data=None)
    if hasattr(msg, 'note') and msg.note == 54 and msg.type == 'note_off':
        mixer.music.stop()
    if hasattr(msg, 'note') and msg.note == 55 and msg.type == 'note_on':
        mixer.music.load('./SleighBells.wav')
        mixer.music.play()
        print(msg)
        print("Color range")
        urllib.request.urlopen('http://10.200.2.137/18/theaterChaseRanger',data=None)
    if hasattr(msg, 'note') and msg.note == 55 and msg.type == 'note_off':
        mixer.music.stop() 
    if hasattr(msg, 'note') and msg.note == 56 and msg.type == 'note_on':
        mixer.music.load('./fluteF6.wav')
        mixer.music.play()
        print(msg)
        print("Red Green Alternate")
        urllib.request.urlopen('http://10.200.2.137/18/Blue',data=None)
    if hasattr(msg, 'note') and msg.note == 56 and msg.type == 'note_off':
        mixer.music.stop()    
    if hasattr(msg, 'note') and msg.note == 57 and msg.type == 'note_on':
        mixer.music.load('./strings.wav')
        mixer.music.play()
        print(msg)
        print("Blue")
        urllib.request.urlopen('http://10.200.2.137/18/rainbowTheaterChase',data=None)
    if hasattr(msg, 'note') and msg.note == 57 and msg.type == 'note_off':
        mixer.music.stop()
    if hasattr(msg, 'note') and msg.note == 58 and msg.type == 'note_on':
        mixer.music.load('./strings.wav')
        mixer.music.play()
        print(msg)
        print("CC")
        urllib.request.urlopen('http://10.200.2.137/18/ccTheaterChase',data=None)
    if hasattr(msg, 'note') and msg.note == 58 and msg.type == 'note_off':
        mixer.music.stop()
    if hasattr(msg, 'note') and msg.note == 59 and msg.type == 'note_on':
        mixer.music.load('./synthc5.wav')
        mixer.music.play()
        print(msg)
        print("yellow blue")
        urllib.request.urlopen('http://10.200.2.137/18/x',data=None)
    if hasattr(msg, 'note') and msg.note == 59 and msg.type == 'note_off':
        mixer.music.stop()           
    if hasattr(msg, 'note') and msg.note == 60 and msg.type == 'note_on':
        mixer.music.load('./synthc6.wav')
        mixer.music.play()
        print(msg)
        print("Candy Cane")
        urllib.request.urlopen('http://10.200.2.137/18/candyCane',data=None)
    if hasattr(msg, 'note') and msg.note == 60 and msg.type == 'note_off':
        mixer.music.stop()
    if hasattr(msg, 'note') and msg.note == 61 and msg.type == 'note_on':
        mixer.music.load('./synthc6.wav')
        mixer.music.play()
        print(msg)
        print("Red/Green/OrangeChase")
        urllib.request.urlopen('http://10.200.2.137/18/theaterChase2',data=None)
    if hasattr(msg, 'note') and msg.note == 61 and msg.type == 'note_off':
        mixer.music.stop()         
    if hasattr(msg, 'note') and msg.note == 62 and msg.type == 'note_on':
        mixer.music.load('./KawaiBellTree.wav')
        mixer.music.play()
        print(msg)
        print("White Theater Chase")
        urllib.request.urlopen('http://10.200.2.137/18/purpleTheaterChase',data=None)
    if hasattr(msg, 'note') and msg.note == 62 and msg.type == 'note_off':
        mixer.music.stop()
    if hasattr(msg, 'note') and msg.note == 63 and msg.type == 'note_on':
        mixer.music.load('./synthc6.wav')
        mixer.music.play()
        print(msg)
        print("TheaterChaseRange")
        urllib.request.urlopen('http://10.200.2.137/18/theaterChaseRanger',data=None)
    if hasattr(msg, 'note') and msg.note == 63 and msg.type == 'note_off':
        mixer.music.stop()
    if hasattr(msg, 'note') and msg.note == 64 and msg.type == 'note_on':
        print(msg)
        print("Silver and Gold")
        urllib.request.urlopen('http://10.200.2.137/18/silverAndGold',data=None)
    if hasattr(msg, 'note') and msg.note == 65 and msg.type == 'note_on':
        mixer.music.load('./bellsA5.wav')
        mixer.music.play()
        print(msg)
        print("OrangeRange")
        urllib.request.urlopen('http://10.200.2.137/18/orangeRange',data=None)
    if hasattr(msg, 'note') and msg.note == 66 and msg.type == 'note_on':
        mixer.music.load('./bellsA5.wav')
        mixer.music.play()
        print(msg)
        print("Tree Test")
        urllib.request.urlopen('http://10.200.2.137/18/treeTest',data=None)
    if hasattr(msg, 'note') and msg.note == 67 and msg.type == 'note_on':
        print(msg)
        print("WhiteBushChase")
        urllib.request.urlopen('http://10.200.2.137/18/whiteBushChase')
    if hasattr(msg, 'note') and msg.note == 68 and msg.type == 'note_on':
        print(msg)
        print("Bush 1 Green and Gold")
        urllib.request.urlopen('http://10.200.2.137/18/bushGreenGold')
    if hasattr(msg, 'note') and msg.note == 69 and msg.type == 'note_on':
        print(msg)
        print("Tree Combo CandyCane Chase")
        urllib.request.urlopen('http://10.200.2.137/18/treeComboChase')
    if hasattr(msg, 'note') and msg.note == 70 and msg.type == 'note_on':
        print(msg)
        print("Pink and Blue Trees")
        urllib.request.urlopen('http://10.200.2.137/18/babyColors')
    if hasattr(msg, 'note') and msg.note == 71 and msg.type == 'note_on':
        print(msg)
        print("Whole Side Orange")
        urllib.request.urlopen('http://10.200.2.137/18/orangeSide')   
    if hasattr(msg, 'note') and msg.note == 72 and msg.type == 'note_on':
        print(msg)
        print("Red 2 Blue")
        urllib.request.urlopen('http://10.200.2.137/18/red2Blue')                     
    if hasattr(msg, 'note') and msg.note == 83 and msg.type == 'note_on':
        print(msg)
        print("Clear colors")
        urllib.request.urlopen('http://10.200.2.137/18/off',data=None)
    if hasattr(msg, 'note') and msg.note == 84 and msg.type == 'note_on':
        mixer.music.load('./KawaiBellTree.wav')
        mixer.music.play()
        print(msg)
        print("White Theater Chase")
        urllib.request.urlopen('http://10.200.2.137/18/whiteTheaterChase',data=None)    
    else:
        print(msg)
