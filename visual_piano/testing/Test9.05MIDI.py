import pygame
import sys
import rtmidi
import random
import math
import mido
import time
# mid = mido.MidiFile('rachc.mid')

# for msg in mid:
#     time.sleep(msg.time)
#     if not msg.is_meta:
#         print(msg)
import time
import rtmidi

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
mid = mido.MidiFile('barbaro.mid')

# if available_ports:
#     midiout.open_port(1)
# else:
#     midiout.open_virtual_port("My virtual output")
ports = mido.get_output_names()
port = mido.open_output(ports[1])

for msg in mid:

    time.sleep(msg.time)
    if not msg.is_meta:
        port.send(msg)

# with midiout:
#     note_on = [0x90, 60, 112] # channel 1, middle C, velocity 112
#     note_off = [0x80, 60, 0]
#     midiout.send_message(note_on)
#     time.sleep(0.5)
#     midiout.send_message(note_off)
#     time.sleep(0.1)
midiout.close_port()

del midiout