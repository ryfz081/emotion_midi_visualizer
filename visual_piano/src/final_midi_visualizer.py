import pygame
import sys
import rtmidi
import random
import math
import mido
import time
import threading
import os
import tkinter as tk
from tkinter import filedialog
import numpy as np
import argparse
import matplotlib.pyplot as plt
import cv2
import random
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
global mid #the midi file
def choose_midi_file():
    global mid
    selected_file = filedialog.askopenfilename(filetypes=[("MIDI Files", "*.mid")])
    
    if selected_file:
        print(f"Selected file: {selected_file}")
        mid = mido.MidiFile(selected_file)
        #print(mid)
        root.destroy()
        # You can work with the selected MIDI file here
        
def on_closing():
    root.destroy()
    sys.exit()
    

global angry
angry = 1
global happy
happy = 1
global sad 
sad = 1

global noteChannel
noteChannel = 144
global pedalChannel
pedalChannel = 176

pygame.init()
# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
video_infos = pygame.display.Info()
#SCREEN_WIDTH, SCREEN_HEIGHT = video_infos.current_w, video_infos.current_h
BAR_COLOR = (0, 255, 0)
BAR_WIDTH = 9 #for notes make it 9
BAR_MAX_HEIGHT = 600  # Maximum height of the bar

def is_Note(message):
    return message[0][0] == 144

def pedal_On(message):
    return message[0][2] != 0 and message[0][0] == pedalChannel
def pedal_Off(message):
    return message[0][2] == 0 and message[0][0] == pedalChannel   
def program_Change(message):
    return message[0][1] == 192

def emotionToColor(emotion):
    # num = random.uniform(emotion**(1/115) - 0.1,emotion**(1/115) + 0.1)
    # if num < 0:
    #     num = random.uniform(0,emotion**(1/115) + 0.1)
    # elif num > 1:
    #     num = random.uniform(emotion**(1/115) - 0.1,1)
    # print("num", num)
    colorValue = emotion**(1/115)
    if colorValue > 235:
        return 235
    return emotion**(1/115)

def process_midi_messages():
    global pedalOn
    for message in mid:
        time.sleep(message.time)
        if not message.is_meta:
            msg = message
            outputPort.send(message)
            if msg.type == 'note_on' or msg.type == 'note_off':
                if msg.velocity > 0:#msg.type == 'note_on':
                    expanding_bars[msg.note-21][0].expanding = True
                    expanding_bars[msg.note-21][1] = msg.velocity
                    if expanding_bars[msg.note-21][0].type == "Dot":
                        expanding_bars[msg.note-21][0].y = map_midi_velocity_to_y(msg.note)
                        

                elif msg.velocity == 0:#msg.type == 'note_off':
                    expanding_bars[msg.note-21][0].expanding = False
                    expanding_bars[msg.note-21][1] = msg.velocity
            elif msg.type == 'control_change': #pedal
                # print(message)
                if msg.control == 64 and msg.value > 0:
                    pedalOn = True
                elif msg.control == 64 and msg.value == 0:
                    pedalOn = False
def process_midi_messages_2():
    global pedalOn
    for message in mid:
        time.sleep(message.time)
        if not message.is_meta:
            msg = message
            if msg.type == 'note_on' or msg.type == 'note_off':
                if  msg.velocity > 0:#msg.type == 'note_on':
                    expanding_bars[msg.note-21][0].expanding = True
                    expanding_bars[msg.note-21][1] = msg.velocity
                    if expanding_bars[msg.note-21][0].type == "Dot":
                        expanding_bars[msg.note-21][0].y = map_midi_velocity_to_y(msg.velocity)


                elif msg.velocity == 0:#msg.type == 'note_off':
                    expanding_bars[msg.note-21][0].expanding = False
                    expanding_bars[msg.note-21][1] = msg.velocity
            elif msg.type == 'control_change': #pedal
                #print(message)
                if msg.control == 64 and msg.value > 0:
                    pedalOn = True
                elif msg.control == 64 and msg.value == 0:
                    pedalOn = False
def detectEmotion():
    global angry
    global happy
    global sad
    while True:
        # Find haar cascade to draw bounding box around face
        ret, frame = cap.read()
        if not ret:
            break
        facecasc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facecasc.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
            prediction = model.predict(cropped_img)
            maxindex = int(np.argmax(prediction))
            if (prediction[0][0]+prediction[0][3] + prediction[0][5] != 0) and (angry != prediction[0][0] or happy != prediction[0][3] or sad != prediction[0][5]):
                # print(angry, happy, sad)  
                angry = prediction[0][0]
                happy = prediction[0][3]
                sad = prediction[0][5]
                
            
            #cv2.putText(frame, emotion_dict[maxindex], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

def map_midi_velocity_to_intensity(velocity):
    # MIDI velocity ranges from 0 to 127
    # Map it to a range of 0 to 255 using a logistic function
    return int(255 / (1 + math.exp(-(velocity - 64) / 16)))
def map_midi_velocity_to_y(midi_value):
    # Ensure the input is within the valid MIDI range
    # Map it to a range of 550 to 50 (reversed) using a logistic growth-like function
    #print("velocity:",midi_value,"height:",int(850 - 805 / (1 + math.exp(-(midi_value - 20) / 50))))
    return int(698 - 659 / (1 + math.exp(-(midi_value - 45) / 22)))
    #return 500

class Particle:
    def __init__(self, x, y, color, velocity, lifetime, direction):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity
        self.lifetime = lifetime
        self.direction = direction  # 'up' or 'down'

    def move(self):
        if self.direction == 'up':
            self.y -= self.velocity
        else:
            self.y += self.velocity
        self.lifetime -= 1

    def draw(self, screen):
        alpha_surface = pygame.Surface((3, 3), pygame.SRCALPHA)
        alpha = int(255 * self.lifetime / 90)  # Fade away over the particle's lifetime
        if alpha > 255:
            alpha = 255
        final_color = self.color + (alpha,)
        pygame.draw.circle(alpha_surface, final_color, (1, 1), 2)
        screen.blit(alpha_surface, (int(self.x), int(self.y)))
BAR_SPEED = 7
class ExpandingBottomBar:
    def __init__(self, x, y):
        self.x = x
        self.bottom_y = y
        self.height = 0
        self.expanding = False
        self.color = (0, 255, 0)
        self.particles = []
        self.type = "BottomBar"

    def expand(self, velocity, pedalOn):
        red = map_midi_velocity_to_intensity(velocity)*emotionToColor(angry) 
        green = map_midi_velocity_to_intensity(velocity)*emotionToColor(happy) 
        blue = map_midi_velocity_to_intensity(velocity)*emotionToColor(sad) 
        if red > 255:
            red = 255
        if blue > 255:
            blue = 255
        if green > 255:
            green = 255
        self.color = (red, blue ,green)
        if self.height < BAR_MAX_HEIGHT:
            self.height += BAR_SPEED
            # Create particles when expanding
            if pedalOn:
                particle_amount = 1
            else:
                particle_amount = 5
            for _ in range(particle_amount):
                particle_x = random.uniform(self.x, self.x + BAR_WIDTH)
                particle_y = random.uniform(self.bottom_y - self.height, self.bottom_y)
                particle_color = self.color
                particle_velocity = random.uniform(1, 5)
                particle_lifetime = random.randint(30, 90)  # Random lifetime between 1 and 3 seconds
                if pedalOn:
                    particle_lifetime = particle_lifetime * 7
                self.particles.append(Particle(particle_x, particle_y, particle_color, particle_velocity, particle_lifetime, 'up'))

    def shrink(self, pedalOn):
        if self.height > 0:
            if pedalOn:
                self.height -= BAR_SPEED * 0.4
            else: 
                self.height -= BAR_SPEED * 7
            # Create fading particles when shrinking
            if pedalOn:
                particle_amount = 1
            else:
                particle_amount = 5
            for _ in range(particle_amount):
                particle_x = random.uniform(self.x, self.x + BAR_WIDTH)
                particle_y = random.uniform(self.bottom_y - self.height, self.bottom_y)
                particle_color = self.color
                particle_velocity = random.uniform(0.1, 2)
                particle_lifetime = random.randint(30, 90)  # Random lifetime between 1 and 3 seconds
                if pedalOn:
                    particle_lifetime = particle_lifetime * 7
                self.particles.append(Particle(particle_x, particle_y, particle_color, particle_velocity, particle_lifetime, 'up'))

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
PARTICLE_MAX_SPEED = 5
PARTICLE_MAX_RADIUS = 5
PARTICLE_MAX_LIFETIME = 60
class ExpandingMiddleBar:
    def __init__(self, x):
        self.middle_x = x
        self.expanding = False
        self.height = 0
        self.color = (0, 255, 0)
        self.particles_up = []  # List for particles moving upwards
        self.particles_down = []  # List for particles moving downwards
        self.type = "MiddleBar"

    def expand(self, velocity, pedalOn):
        red = map_midi_velocity_to_intensity(velocity)*emotionToColor(angry) 
        green = map_midi_velocity_to_intensity(velocity)*emotionToColor(happy) 
        blue = map_midi_velocity_to_intensity(velocity)*emotionToColor(sad) 
        if red > 255:
            red = 255
        if blue > 255:
            blue = 255
        if green > 255:
            green = 255
        self.color = (red, blue ,green)
        if self.height < (SCREEN_HEIGHT // 2):
            self.height += BAR_SPEED

            # Create particles when expanding (upward)
            if pedalOn:
                particle_amount = 1
            else:
                particle_amount = 5
            for _ in range(particle_amount):
                particle_x = random.uniform(self.middle_x - BAR_WIDTH // 2, self.middle_x + BAR_WIDTH // 2)
                particle_y = random.uniform((SCREEN_HEIGHT // 2) - self.height, (SCREEN_HEIGHT // 2))
                particle_color = self.color
                particle_velocity = random.uniform(1, PARTICLE_MAX_SPEED)
                particle_lifetime = random.randint(30, PARTICLE_MAX_LIFETIME)
                if pedalOn:
                    particle_lifetime = particle_lifetime * 3
                self.particles_up.append(Particle(particle_x, particle_y, particle_color, particle_velocity, particle_lifetime, 'up'))

            # Create particles when expanding (downward)
            if pedalOn:
                particle_amount = 1
            else:
                particle_amount = 5
            for _ in range(particle_amount):
                particle_x = random.uniform(self.middle_x - BAR_WIDTH // 2, self.middle_x + BAR_WIDTH // 2)
                particle_y = random.uniform((SCREEN_HEIGHT // 2), (SCREEN_HEIGHT // 2) + self.height)
                particle_color = self.color
                particle_velocity = random.uniform(1, PARTICLE_MAX_SPEED)
                particle_lifetime = random.randint(30, PARTICLE_MAX_LIFETIME)
                if pedalOn:
                    particle_lifetime = particle_lifetime * 3
                self.particles_down.append(Particle(particle_x, particle_y, particle_color, particle_velocity, particle_lifetime, 'down'))

    def shrink(self, pedalOn):
        if self.height > 0:
            if pedalOn:
                self.height -= BAR_SPEED * 0.4
            else: 
                self.height -= BAR_SPEED * 7
            # Create particles when expanding (upward)
            if pedalOn:
                particle_amount = 1
            else:
                particle_amount = 5
            for _ in range(particle_amount):
                particle_x = random.uniform(self.middle_x - BAR_WIDTH // 2, self.middle_x + BAR_WIDTH // 2)
                particle_y = random.uniform((SCREEN_HEIGHT // 2) - self.height, (SCREEN_HEIGHT // 2))
                particle_color = self.color
                particle_velocity = random.uniform(1, PARTICLE_MAX_SPEED)
                particle_lifetime = random.randint(30, PARTICLE_MAX_LIFETIME)
                if pedalOn:
                    particle_lifetime = particle_lifetime * 3
                self.particles_up.append(Particle(particle_x, particle_y, particle_color, particle_velocity, particle_lifetime, 'up'))

            # Create particles when expanding (downward)
            if pedalOn:
                particle_amount = 1
            else:
                particle_amount = 5
            for _ in range(particle_amount):
                particle_x = random.uniform(self.middle_x - BAR_WIDTH // 2, self.middle_x + BAR_WIDTH // 2)
                particle_y = random.uniform((SCREEN_HEIGHT // 2), (SCREEN_HEIGHT // 2) + self.height)
                particle_color = self.color
                particle_velocity = random.uniform(1, PARTICLE_MAX_SPEED)
                particle_lifetime = random.randint(30, PARTICLE_MAX_LIFETIME)
                if pedalOn:
                    particle_lifetime = particle_lifetime * 3
                self.particles_down.append(Particle(particle_x, particle_y, particle_color, particle_velocity, particle_lifetime, 'down'))

    def update_particles(self):
        new_particles_up = []
        new_particles_down = []
        for particle in self.particles_up:
            particle.move()
            if particle.lifetime > 0:
                new_particles_up.append(particle)
        self.particles_up = new_particles_up

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

        top_y = (SCREEN_HEIGHT // 2) - self.height
        bottom_y = (SCREEN_HEIGHT // 2) + self.height
        pygame.draw.rect(screen, self.color, (self.middle_x - BAR_WIDTH // 2, top_y, BAR_WIDTH, 2 * self.height))

    def setColor(self, color):
        self.color = color
DOT_COLOR = (0, 255, 0)
DOT_RADIUS = 10
DOT_MAX_RADIUS = 20
DOT_PULSE_SPEED = 1
Y_POSITION_RANGE = (50, 550)  # Adjust the Y position range as needed

class ExpandingDot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 0
        self.expanding = False
        self.visible = False
        self.color = DOT_COLOR
        self.type = "Dot"

    def expand(self, velocity, pedalOn):
        red = map_midi_velocity_to_intensity(velocity)*emotionToColor(angry) 
        green = map_midi_velocity_to_intensity(velocity)*emotionToColor(happy) 
        blue = map_midi_velocity_to_intensity(velocity)*emotionToColor(sad) 
        if red > 255:
            red = 255
        if blue > 255:
            blue = 255
        if green > 255:
            green = 255
        self.color = (red, blue ,green)
        if self.radius < DOT_MAX_RADIUS:
            self.radius += DOT_PULSE_SPEED*5
            self.visible = True

    def shrink(self, pedalOn):
        if self.radius > 0:
            if pedalOn:
                self.radius -= DOT_PULSE_SPEED 
            else:
                self.radius -= DOT_PULSE_SPEED
            if self.radius <= 0:
                self.visible = False


    def draw(self, screen):
        if self.visible:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))

# Define data generators
val_dir = 'data/test'

num_train = 28709
num_val = 7178
batch_size = 64
num_epoch = 50

val_datagen = ImageDataGenerator(rescale=1./255)

validation_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=(48,48),
        batch_size=batch_size,
        color_mode="grayscale",
        class_mode='categorical')

# Create the model
model = Sequential()

model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax'))

# emotions will be displayed on your face from the webcam feed
model.load_weights('model.h5')

# prevents openCL usage and unnecessary logging messages
cv2.ocl.setUseOpenCL(False)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE| pygame.SCALED) #pygame.RESIZABLE | pygame.SCALED)
pygame.display.set_caption("Piano Visualizer")


# Main game loop
running = True
clock = pygame.time.Clock()
midiin = rtmidi.MidiIn()
ports = range(midiin.get_port_count())
global pedalOn
pedalOn = False #this is a boolean if pedal is on

# dictionary which assigns each label an emotion (alphabetical order)
emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
# start the webcam feed
cap = cv2.VideoCapture(0)

print("1: BottomBar, 2: MiddleBar, 3: Dots")
visualPreset = int(input())
dotPedalEffect = 0
# List to hold the expanding bars
#expanding_bars = [[bar1, 0], [bar2, 0], [bar3, 0]] #bar, velocity

if visualPreset == 1:
    expanding_bars = [[ExpandingBottomBar(9*(i-20), SCREEN_HEIGHT), 0] for i in range(21,109)]
    print("Blend Mode On? (1: Yes, Any Number: No)")
    blendMode = int(input())
    if blendMode == 1:
        dotPedalEffect = 5
if visualPreset == 2:
    expanding_bars = [[ExpandingMiddleBar(9*(i-20)), 0] for i in range(21,109)]
    print("Pedal Blend Mode On? (1: Yes, Any Number: No)")
    blendMode = int(input())
    if blendMode == 1:
        dotPedalEffect = 5
if visualPreset == 3:
    expanding_bars = [[ExpandingDot(9*(i-20), 100), 0] for i in range(21,109)]
    dotPedalEffect = 5
    
print(midiin.get_ports())
print("1: Live MIDI Input, 2: Select MIDI File for MIDI Output, 3: Select MIDI File without MIDI Output")
visualizerMode = int(input())
if visualizerMode==1: #if midi has inputport
    print("input")
    midiin.open_port(0)
    emotion_thread = threading.Thread(target=detectEmotion)
    emotion_thread.start()
    print("---Callibration---")
    print("1. Press any Note") 
    while running: 
        a = midiin.get_message()
        if a:
            noteChannel = a[0][0] 
            print(noteChannel) 
            break
    print("2. Step on the Pedal (if no pedal then press any note)")  
    while running:
        b = midiin.get_message()
        if b and b[0][2] != 0:
            if b and b[0][0] != noteChannel:
                pedalChannel = b[0][0]  
                print(b)
                break
            elif b and b[0][0] == noteChannel:
                print(b)
                break
    while running:
        m = midiin.get_message()
        if m:
            if m[0][2] > 0 and m[0][0] == noteChannel:
                expanding_bars[m[0][1] - 21][0].expanding = True
                expanding_bars[m[0][1] - 21][1] = m[0][2]
                if visualPreset == 3:
                    #print("HEYY")
                    expanding_bars[m[0][1]-21][0].y = map_midi_velocity_to_y(m[0][2])
            elif m[0][2] == 0 and m[0][0] == noteChannel:
                expanding_bars[m[0][1] - 21][0].expanding = False
                expanding_bars[m[0][1] - 21][1] = m[0][2]

            else: #pedal
                #print("im printing here")
                if pedal_On(m):
                    pedalOn = True
                elif pedal_Off(m):
                    pedalOn = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("quit")
                running = False
                midiin.close_port()
        # Update the expanding bars
        for bar in expanding_bars:
            if bar[0].expanding:
                print(bar[1], pedalOn)
                bar[0].expand(bar[1], pedalOn) #bar[0] is actual bar object, bar[1] is the velocity
            else:
                bar[0].shrink(pedalOn)

        # Clear the screen
        if pedalOn:
            #print("ayo pedal on")
            screen.fill((int(emotionToColor(angry))*20,int(emotionToColor(happy))*20,int(emotionToColor(sad))*20), special_flags=dotPedalEffect)
        else:
            #print("pedal off")
            screen.fill((int(emotionToColor(angry))*20,int(emotionToColor(happy))*20,int(emotionToColor(sad))*20))


        # Draw the expanding bars
        for bar in expanding_bars:
            bar[0].draw(screen)

        # Update the display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(60)

    # Quit the game
    cap.release()
    cv2.destroyAllWindows()
    emotion_thread.join()
    pygame.quit()
    sys.exit()
else:
    #MIDI File Choosing Dialog
    root = tk.Tk()
    root.title("Choose MIDI File")
    root.attributes("-topmost", True)
    # Calculate the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the window's width and height
    window_width = 400
    window_height = 150

    # Center the window on the screen
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Make the button bigger
    button = tk.Button(root, text="Choose MIDI File", command=choose_midi_file, height=3, width=20)
    button.pack(pady=20)

    root.protocol("WM_DELETE_WINDOW", on_closing)  # Close button event
    root.mainloop()
    # End of MIDI File Choosing Dialog len(mido.get_output_names()) > 1
    if visualizerMode == 2:
        #print("bros")

        outputPorts = mido.get_output_names()
        outputPort = mido.open_output(outputPorts[1])
        #print("bros2")
        
        # Create a thread for MIDI processing
        midi_thread = threading.Thread(target=process_midi_messages)
        midi_thread.start()
        # Create a thread for Emotion Detection
        emotion_thread = threading.Thread(target=detectEmotion)
        emotion_thread.start()
        # Main loop
        running = True
        pedalOn = False  # Your pedal state variable

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


            # Update the expanding bars
            for bar in expanding_bars:
                if bar[0].expanding:
                    bar[0].expand(bar[1], pedalOn)
                else:
                    bar[0].shrink(pedalOn)
                    

            # Clear the screen
            if pedalOn:
                screen.fill((int(emotionToColor(angry))*20,int(emotionToColor(happy))*20,int(emotionToColor(sad))*20), special_flags=dotPedalEffect)
            else:
                screen.fill((int(emotionToColor(angry))*20,int(emotionToColor(happy))*20,int(emotionToColor(sad))*20))


            # Draw the expanding bars
            for bar in expanding_bars:
                bar[0].draw(screen)

            # Update the display
            pygame.display.flip()

            # # Start the MIDI processing thread (if not already started)
            # if not midi_thread.is_alive():
            #     midi_thread.start()

            # Limit the frame rate
            clock.tick(60)



        # Quit Pygame
        pygame.quit()
        os._exit(1)
        midi_thread.join()
        sys.exit(0)
    elif visualizerMode == 3:
        #print("mmm")
        midi_thread = threading.Thread(target=process_midi_messages_2)
        midi_thread.start()
        # Create a thread for Emotion Detection
        emotion_thread = threading.Thread(target=detectEmotion)
        emotion_thread.start()
        # Main loop
        running = True
        pedalOn = False  # Your pedal state variable

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update the expanding bars
            for bar in expanding_bars:
                if bar[0].expanding:
                    bar[0].expand(bar[1], pedalOn)
                else:
                    bar[0].shrink(pedalOn)
                    

            # Clear the screen
            if pedalOn:
                #print("pedalOn", (int(emotionToColor(angry))*20,int(emotionToColor(happy))*20,int(emotionToColor(sad))*20))
                #print("ayo", (int(emotionToColor(angry))*20,int(emotionToColor(happy))*20,int(emotionToColor(sad))*20))
                screen.fill((int(emotionToColor(angry))*20,int(emotionToColor(happy))*20,int(emotionToColor(sad))*20), special_flags=dotPedalEffect)
            else:
                #print("pedalOff")
                screen.fill((int(emotionToColor(angry))*20,int(emotionToColor(happy))*20,int(emotionToColor(sad))*20))


            # Draw the expanding bars
            for bar in expanding_bars:
                bar[0].draw(screen)

            # Update the display
            pygame.display.flip()

            # # Start the MIDI processing thread (if not already started)
            # if not midi_thread.is_alive():
            #     midi_thread.start()

            # Limit the frame rate
            clock.tick(60)



        # Quit Pygame
        pygame.quit()
        os._exit(1)
        midi_thread.join()
        sys.exit(0)   

    


