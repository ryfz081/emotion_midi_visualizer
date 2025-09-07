import pygame
import tkinter as tk
from tkinter import filedialog
import sys
import mido

from midi2audio import FluidSynth

#Play MIDI

#FluidSynth().play_midi("rachc.mid")

#Synthesize MIDI to audio

# Note: the default sound font is in 44100 Hz sample rate

fs = FluidSynth()
fs.midi_to_audio('rachc.mid', 'output.wav')

# FLAC, a lossless codec, is recommended

fs.midi_to_audio('rachc.mid', 'output.flac')