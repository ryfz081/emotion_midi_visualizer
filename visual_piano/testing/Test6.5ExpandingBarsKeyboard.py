import pygame
import sys
import rtmidi
import random
# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BAR_COLOR = (0, 255, 0)
BAR_WIDTH = 25 #for notes make it 9
BAR_MAX_HEIGHT = 600  # Maximum height of the bar
BAR_SPEED = 15
def is_Note(message):
    return message[0][0] == 144

def is_On(message):
    return message[0][2] != 0
class ExpandingBottomBar:
    def __init__(self, x, y):
        self.x = x
        self.bottom_y = y
        self.height = 0
        self.expanding = False
        self.color = (0,255,0)
    def expand(self, velocity):
        #self.color = (50,velocity*2,50)
        self.color = velocity
        if self.height < BAR_MAX_HEIGHT:
            self.height += BAR_SPEED

    def shrink(self):
        if self.height > 0:
            self.height -= BAR_SPEED * 7

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.bottom_y - self.height, BAR_WIDTH, self.height))
        
    def setColor(self, color):
        self.color = color

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Expanding Bars")

# Create two instances of ExpandingBottomBar
# bar1 = ExpandingBottomBar(100, SCREEN_HEIGHT)
# bar2 = ExpandingBottomBar(300, SCREEN_HEIGHT)
# bar3 = ExpandingBottomBar(500, SCREEN_HEIGHT)
# bar2 = ExpandingBottomBar(300, SCREEN_HEIGHT)
# bar2 = ExpandingBottomBar(300, SCREEN_HEIGHT)

# List to hold the expanding bars
#expanding_bars = [[bar1, 0], [bar2, 0], [bar3, 0]] #bar, velocity
expanding_bars = [[ExpandingBottomBar(9*(i-20), SCREEN_HEIGHT), 0] for i in range(21,109)]

# Main game loop
running = True
clock = pygame.time.Clock()
midiin = rtmidi.MidiIn()
ports = range(midiin.get_port_count())
pedalOn = False #this is a boolean if pedal is on
#lookupTable = {pygame.K_q:10, pygame.K_w:20, pygame.K_e:30, pygame.K_r:40, pygame.K_t:50, pygame.K_y:60, pygame.K_u:70, pygame.K_i:80, pygame.K_o:90, pygame.K_p:100,}
# if ports: #if midi has port
#midiin.open_port(0)
testingColor = "white"
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

    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        testingColor = "red"
    if keys[pygame.K_2]:
        testingColor = "blue"
    if keys[pygame.K_3]:
        testingColor = "yellow"
    if keys[pygame.K_4]:
        testingColor = "white"
    if keys[pygame.K_5]:
        testingColor = "black"

    if keys[pygame.K_q]:
        expanding_bars[0][0].expanding = True
    else:
        expanding_bars[0][0].expanding = False
    if keys[pygame.K_w]:
        expanding_bars[10][0].expanding = True
    else:
        expanding_bars[10][0].expanding = False
    if keys[pygame.K_e]:
        expanding_bars[20][0].expanding = True
    else:
        expanding_bars[20][0].expanding = False
    if keys[pygame.K_r]:
        expanding_bars[30][0].expanding = True
    else:
        expanding_bars[30][0].expanding = False
    if keys[pygame.K_t]:
        expanding_bars[40][0].expanding = True
    else:
        expanding_bars[40][0].expanding = False
    if keys[pygame.K_y]:
        expanding_bars[50][0].expanding = True
    else:
        expanding_bars[50][0].expanding = False
    if keys[pygame.K_u]:
        expanding_bars[60][0].expanding = True
    else:
        expanding_bars[60][0].expanding = False
    if keys[pygame.K_i]:
        expanding_bars[70][0].expanding = True
    else:
        expanding_bars[70][0].expanding = False
    if keys[pygame.K_o]:
        expanding_bars[80][0].expanding = True
    else:
        expanding_bars[80][0].expanding = False
    if keys[pygame.K_p]:
        expanding_bars[87][0].expanding = True
    else:
        expanding_bars[87][0].expanding = False
        
    
    
        
    # Update the expanding bars
    for bar in expanding_bars:
        if bar[0].expanding:
            bar[0].expand(testingColor)#bar[1]) #bar[0] is actual bar object, bar[1] is the velocity
        else:
            bar[0].shrink()

    # Clear the screen
    if pedalOn or keys[pygame.K_0]:
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

d