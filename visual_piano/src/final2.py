import pygame
import sys
import rtmidi
import math
import mido
import time
import threading
import tkinter as tk
from tkinter import filedialog
import numpy as np
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Suppress TensorFlow logs
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

global mid

def choose_midi_file():
    global mid
    selected_file = filedialog.askopenfilename(filetypes=[("MIDI Files", "*.mid")])
    if selected_file:
        print(f"Selected file: {selected_file}")
        mid = mido.MidiFile(selected_file)
        root.destroy()

def on_closing():
    root.destroy()
    sys.exit()

# Global emotion variables
global angry, happy, sad
angry = 50
happy = 50
sad = 50

# MIDI channels
global noteChannel, pedalChannel
noteChannel = 144
pedalChannel = 176

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BAR_COLOR = (0, 255, 0)
BAR_WIDTH = 9
BAR_MAX_HEIGHT = 600
BAR_SPEED = 15

def emotionToColor(emotion):
    colorValue = emotion ** (1/115)
    if colorValue > 235:
        return 235
    return colorValue

def detectEmotion():
    global angry, happy, sad
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facecasc.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
            prediction = model.predict(cropped_img)
            angry = prediction[0][0]
            happy = prediction[0][3]
            sad = prediction[0][5]
    cap.release()
    cv2.destroyAllWindows()

# Initialize TensorFlow model for emotion detection
model = Sequential([
    Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)),
    Conv2D(64, kernel_size=(3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),
    Conv2D(128, kernel_size=(3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(128, kernel_size=(3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),
    Flatten(),
    Dense(1024, activation='relu'),
    Dropout(0.5),
    Dense(7, activation='softmax')
])
model.load_weights('model.h5')

facecasc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

class Particle:
    def __init__(self, x, y, color, velocity, lifetime, direction):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity
        self.lifetime = lifetime
        self.direction = direction

    def move(self):
        if self.direction == 'up':
            self.y -= self.velocity
        else:
            self.y += self.velocity
        self.lifetime -= 1

    def draw(self, screen):
        alpha_surface = pygame.Surface((3, 3), pygame.SRCALPHA)
        alpha = int(255 * self.lifetime / 90)
        final_color = self.color + (alpha,)
        pygame.draw.circle(alpha_surface, final_color, (1, 1), 2)
        screen.blit(alpha_surface, (int(self.x), int(self.y)))

class ExpandingBottomBar:
    def __init__(self, x, y):
        self.x = x
        self.bottom_y = y
        self.height = 0
        self.expanding = False
        self.color = (0, 255, 0)
        self.particles = []

    def expand(self, velocity):
        red = map_midi_velocity_to_intensity(velocity) * emotionToColor(angry)
        green = map_midi_velocity_to_intensity(velocity) * emotionToColor(happy)
        blue = map_midi_velocity_to_intensity(velocity) * emotionToColor(sad)
        self.color = (min(255, red), min(255, blue), min(255, green))
        if self.height < BAR_MAX_HEIGHT:
            self.height += BAR_SPEED
            for _ in range(5):
                particle_x = random.uniform(self.x, self.x + BAR_WIDTH)
                particle_y = random.uniform(self.bottom_y - self.height, self.bottom_y)
                self.particles.append(Particle(particle_x, particle_y, self.color, random.uniform(1, 5), random.randint(30, 90), 'up'))

    def shrink(self):
        if self.height > 0:
            self.height -= BAR_SPEED * 7
            for _ in range(5):
                particle_x = random.uniform(self.x, self.x + BAR_WIDTH)
                particle_y = random.uniform(self.bottom_y - self.height, self.bottom_y)
                self.particles.append(Particle(particle_x, particle_y, self.color, random.uniform(0.1, 2), random.randint(30, 90), 'up'))

    def update_particles(self):
        new_particles = []
        for particle in self.particles:
            particle.move()
            if particle.lifetime > 0:
                new_particles.append(particle)
        self.particles = new_particles

    def draw(self, screen):
        self.update_particles()
        for particle in self.particles:
            particle.draw(screen)
        pygame.draw.rect(screen, self.color, (self.x, self.bottom_y - self.height, BAR_WIDTH, self.height))

class ExpandingMiddleBar:
    def __init__(self, x):
        self.middle_x = x
        self.expanding = False
        self.height = 0
        self.color = (0, 255, 0)
        self.particles_up = []
        self.particles_down = []

    def expand(self, velocity):
        red = map_midi_velocity_to_intensity(velocity) * emotionToColor(angry)
        green = map_midi_velocity_to_intensity(velocity) * emotionToColor(happy)
        blue = map_midi_velocity_to_intensity(velocity) * emotionToColor(sad)
        self.color = (min(255, red), min(255, blue), min(255, green))
        if self.height < (SCREEN_HEIGHT // 2):
            self.height += BAR_SPEED
            for _ in range(10):
                particle_x = random.uniform(self.middle_x - BAR_WIDTH // 2, self.middle_x + BAR_WIDTH // 2)
                particle_y = random.uniform((SCREEN_HEIGHT // 2) - self.height, (SCREEN_HEIGHT // 2))
                self.particles_up.append(Particle(particle_x, particle_y, self.color, random.uniform(1, 5), random.randint(30, 90), 'up'))
            for _ in range(10):
                particle_x = random.uniform(self.middle_x - BAR_WIDTH // 2, self.middle_x + BAR_WIDTH // 2)
                particle_y = random.uniform((SCREEN_HEIGHT // 2), (SCREEN_HEIGHT // 2) + self.height)
                self.particles_down.append(Particle(particle_x, particle_y, self.color, random.uniform(1, 5), random.randint(30, 90), 'down'))

    def shrink(self):
        if self.height > 0:
            self.height -= BAR_SPEED * 7
            for _ in range(10):
                particle_x = random.uniform(self.middle_x - BAR_WIDTH // 2, self.middle_x + BAR_WIDTH // 2)
                particle_y = random.uniform((SCREEN_HEIGHT // 2) - self.height, (SCREEN_HEIGHT // 2))
                self.particles_up.append(Particle(particle_x, particle_y, self.color, random.uniform(0.1, 2), random.randint(30, 90), 'up'))
            for _ in range(10):
                particle_x = random.uniform(self.middle_x - BAR_WIDTH // 2, self.middle_x + BAR_WIDTH // 2)
                particle_y = random.uniform((SCREEN_HEIGHT // 2), (SCREEN_HEIGHT // 2) + self.height)
                self.particles_down.append(Particle(particle_x, particle_y, self.color, random.uniform(0.1, 2), random.randint(30, 90), 'down'))

    def update_particles(self):
        new_particles_up = []
        for particle in self.particles_up:
            particle.move()
            if particle.lifetime > 0:
                new_particles_up.append(particle)
        self.particles_up = new_particles_up
        new_particles_down = []
        for particle in self.particles_down:
            particle.move()
            if particle.lifetime > 0:
                new_particles_down.append(particle)
        self.particles_down = new_particles_down

    def draw(self, screen):
        self.update_particles()
        for particle in self.particles_up:
            particle.draw(screen)
        for particle in self.particles_down:
            particle.draw(screen)
        pygame.draw.rect(screen, self.color, (self.middle_x - BAR_WIDTH // 2, (SCREEN_HEIGHT // 2) - self.height, BAR_WIDTH, self.height * 2))

noteBars = []
for x in range(0, SCREEN_WIDTH, BAR_WIDTH + 1):
    noteBars.append(ExpandingBottomBar(x, SCREEN_HEIGHT))

pedalBars = []
for x in range(0, SCREEN_WIDTH, (BAR_WIDTH + 1) * 3):
    pedalBars.append(ExpandingMiddleBar(x + (BAR_WIDTH // 2)))

def map_midi_note_to_x(note):
    note -= 20
    return note * 4.72

def map_midi_velocity_to_intensity(velocity):
    return velocity

root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.withdraw()
root.call('wm', 'attributes', '.', '-topmost', '1')
choose_midi_file()
root.mainloop()

def playMIDI():
    midiout = rtmidi.MidiOut()
    midiout.open_virtual_port("My virtual output")

    for i, track in enumerate(mid.tracks):
        for msg in track:
            time.sleep(msg.time)
            if msg.type == 'note_on':
                midiout.send_message(msg.bytes())
                x = map_midi_note_to_x(msg.note)
                barIndex = int(x // (BAR_WIDTH + 1))
                if barIndex >= 0 and barIndex < len(noteBars):
                    noteBars[barIndex].expand(msg.velocity)
            if msg.type == 'note_off':
                x = map_midi_note_to_x(msg.note)
                barIndex = int(x // (BAR_WIDTH + 1))
                if barIndex >= 0 and barIndex < len(noteBars):
                    noteBars[barIndex].shrink()
            if msg.type == 'control_change' and msg.control == 64:
                for bar in pedalBars:
                    if msg.value > 0:
                        bar.expand(msg.value)
                    else:
                        bar.shrink()

midi_thread = threading.Thread(target=playMIDI)
emotion_thread = threading.Thread(target=detectEmotion)

midi_thread.start()
emotion_thread.start()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Piano Visualizer")

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((0, 0, 0))
    for bar in noteBars:
        bar.draw(screen)
    for bar in pedalBars:
        bar.draw(screen)
    pygame.display.flip()
    clock.tick(30)
