import pygame
import sys
import rtmidi
import random
import time
import math
# Initialize pygame
pygame.init()
# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BAR_COLOR = (0, 255, 0)
BAR_WIDTH = 9 #for notes make it 9
BAR_MAX_HEIGHT = 600  # Maximum height of the bar
BAR_SPEED = 15
def is_Note(message):
    return message[0][0] == 144

def is_On(message):
    return message[0][2] != 0

def map_midi_velocity_to_intensity(velocity):
    # MIDI velocity ranges from 0 to 127
    # Map it to a range of 0 to 255 using a logistic function
    return int(255 / (1 + math.exp(-(velocity - 64) / 16)))
class Particle:
    def __init__(self, x, y, color, velocity, lifetime):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity
        self.lifetime = lifetime

    def move(self):
        self.y -= self.velocity
        self.lifetime -= 1

    def draw(self, screen):
        alpha_surface = pygame.Surface((3, 3), pygame.SRCALPHA)
        alpha = int(255 * self.lifetime / 90)  # Fade away over the particle's lifetime
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
        self.color = (30, 20, map_midi_velocity_to_intensity(velocity))
        if self.height < BAR_MAX_HEIGHT:
            self.height += BAR_SPEED
            # Create particles when expanding
            # for _ in range(10):
            #     particle_x = random.uniform(self.x, self.x + BAR_WIDTH)
            #     particle_y = random.uniform(self.bottom_y - self.height, self.bottom_y)
            #     particle_color = self.color
            #     particle_velocity = random.uniform(1, 5)
            #     particle_lifetime = random.randint(30, 90)  # Random lifetime between 1 and 3 seconds
            #     self.particles.append(Particle(particle_x, particle_y, particle_color, particle_velocity, particle_lifetime))

    def shrink(self):
        if self.height > 0:
            self.height -= BAR_SPEED * 7
            # Create fading particles when shrinking
            for _ in range(10):
                particle_x = random.uniform(self.x, self.x + BAR_WIDTH)
                particle_y = random.uniform(self.bottom_y - self.height, self.bottom_y)
                particle_color = self.color
                particle_velocity = random.uniform(0.1, 2)
                particle_lifetime = random.randint(30, 90)  # Random lifetime between 1 and 3 seconds
                self.particles.append(Particle(particle_x, particle_y, particle_color, particle_velocity, particle_lifetime))

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


# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)
pygame.display.set_caption("Expanding Bars")


# List to hold the expanding bars
#expanding_bars = [[bar1, 0], [bar2, 0], [bar3, 0]] #bar, velocity
expanding_bars = [[ExpandingBottomBar(9*(i-20), SCREEN_HEIGHT), 0] for i in range(21,109)]

# Main game loop
running = True
clock = pygame.time.Clock()
midiin = rtmidi.MidiIn()
ports = range(midiin.get_port_count())
pedalOn = False #this is a boolean if pedal is on

if ports: #if midi has port
    midiin.open_port(0)
    while running:
        m = midiin.get_message()
        if m:
            # print(m)
            if m[0][2] > 0:
                expanding_bars[m[0][1] - 21][0].expanding = True
                expanding_bars[m[0][1] - 21][1] = m[0][2]
            elif m[0][2] == 0:
                expanding_bars[m[0][1] - 21][0].expanding = False
                expanding_bars[m[0][1] - 21][1] = m[0][2]
                    
                # if is_On(m) and m[0][1] == 64:
                #     expanding_bars[1][0].expanding = True
                #     expanding_bars[1][1] = m[0][2]
                # elif not is_On(m) and m[0][1] == 64 :
                #     expanding_bars[1][0].expanding = False
                #     expanding_bars[1][1] = m[0][2]
                    
                # if is_On(m) and m[0][1] == 67:
                #     expanding_bars[2][0].expanding = True
                #     expanding_bars[2][1] = m[0][2]
                # elif not is_On(m) and m[0][1] == 67 :
                #     expanding_bars[2][0].expanding = False
                #     expanding_bars[2][1] = m[0][2]
            else: #pedal
                if is_On(m):
                    pedalOn = True
                else:
                    pedalOn = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("bro")
                running = False
                midiin.close_port()


            
        
        
            
        # Update the expanding bars
        for bar in expanding_bars:
            if bar[0].expanding:
                bar[0].expand(bar[1]) #bar[0] is actual bar object, bar[1] is the velocity
            else:
                bar[0].shrink()

        # Clear the screen
        # if pedalOn:

        #     screen.fill((0,20,100))
        # else:
        screen.fill((50, 50, 50))

        # Draw the expanding bars
        for bar in expanding_bars:
            bar[0].draw(screen)

        # Update the display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(60)

    # Quit the game
    pygame.quit()
    sys.exit()

