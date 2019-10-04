#mido is the library that handles MIDI I/O
import mido
import RPi.GPIO as GPIO
#Setting the backend for the file due to issues installing the default backend
mido.set_backend('mido.backends.portmidi')

#use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BCM)

#set channel for output
GPIO.setup(18, GPIO.OUT)

#for debug purposes print backend on program start
print(mido.backend)
print(mido.get_input_names())

inport = mido.open_input('AKM320 MIDI 1')
msg = inport.receive()
#This loop constantly checks for new messages coming into the port
for msg in inport:
   #check for the correct attribute to assign an action to the msg
   #in this instance we are checking for the note attribute to assign
   #the note name to the note itself, and only on note_on msg types
    if hasattr(msg, 'note') and msg.note == 53 and msg.type == 'note_on':
        print("This is the low F")
	GPIO.output(18, GPIO.HIGH)
        print(msg)
    elif hasattr(msg, 'note') and msg.note == 53 and msg.type == 'note_off':
	print("Turning off")
	GPIO.output(18, GPIO.LOW)
    elif hasattr(msg, 'note') and msg.note == 84 and msg.type == 'note_on':
        print("This is the high C")
        print(msg)
    elif hasattr(msg, 'note') and msg.note == 55 and msg.type == 'note_on':
	print("This is low G")
	print(msg)
    else:
        print(msg)
#TODO bind different keys to different functions just to test functionality.
        #start experimenting with connecting lights to pi.
