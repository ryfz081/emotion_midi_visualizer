import pygame
import sys
import rtmidi
import random
import math
# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BAR_COLOR = (0, 255, 0)
BAR_WIDTH = 9 #for notes make it 9
BAR_MAX_HEIGHT = 600  # Maximum height of the bar
BAR_SPEED = 7
def is_Note(message):
    return message[0][0] == 144

def is_On(message):
    return message[0][2] != 0
def map_midi_velocity_to_intensity(velocity):
    # MIDI velocity ranges from 0 to 127
    # Map it to a range of 0 to 255 using a logistic function
    return int(255 / (1 + math.exp(-(velocity - 64) / 16)))
class ExpandingMiddleBar:
    def __init__(self, x):
        self.middle_x = x
        self.expanding = False
        self.height = 0
        self.color = (0, 255, 0)

    def expand(self, velocity):
        self.color = (50, map_midi_velocity_to_intensity(velocity), 50)
        if self.height < (SCREEN_HEIGHT // 2):
            self.height += BAR_SPEED

    def shrink(self):
        if self.height > 0:
            self.height -= BAR_SPEED * 7

    def draw(self, screen):
        top_y = SCREEN_HEIGHT // 2 - self.height
        bottom_y = SCREEN_HEIGHT // 2 + self.height
        pygame.draw.rect(screen, self.color, (self.middle_x - BAR_WIDTH // 2, top_y, BAR_WIDTH, 2 * self.height))

    def setColor(self, color):
        self.color = color




# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Expanding Bars")


# List to hold the expanding bars
#expanding_bars = [[bar1, 0], [bar2, 0], [bar3, 0]] #bar, velocity
expanding_bars = [[ExpandingMiddleBar(9*(i-20)), 0] for i in range(21,109)]

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
            if is_Note(m):
                if is_On(m): #m[0][1] is midi note value
                    expanding_bars[m[0][1]-21][0].expanding = True
                    expanding_bars[m[0][1]-21][1] = m[0][2]
                elif not is_On(m):
                    expanding_bars[m[0][1]-21][0].expanding = False
                    expanding_bars[m[0][1]-21][1] = m[0][2]
                    
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
        if pedalOn:
            screen.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        else:
            screen.fill((0, 0, 0))

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

