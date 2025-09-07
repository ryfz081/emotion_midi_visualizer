import pygame
import pygame_gui
from pygame_gui.core import ObjectID


pygame.init()

pygame.display.set_caption('Quick Start')
interface = pygame.display.set_mode((800, 600), pygame.RESIZABLE | pygame.SCALED) 
background = pygame.Surface((800, 600))
background.fill(pygame.Color('#434343ff'))

manager = pygame_gui.UIManager((800, 600), 'theme.json')


side_panel = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect(0, 0, 180, 600), manager=manager)




playButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((330, 398), (75, 75)),
                                            text='Play',
                                            manager=manager, object_id=ObjectID(class_id="@circle_buttons", object_id="#play_button"))

pauseButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((380, 398), (75, 75)),
                                            text='Pause',
                                            manager=manager, object_id=ObjectID(class_id="@circle_buttons", object_id="#pause_button"))

stopButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 398), (75, 75)),
                                            text='Stop',
                                            manager=manager, object_id=ObjectID(class_id="@circle_buttons", object_id="#stop_button"))

MIDIButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((430, 398), (75, 75)),
                                            text='Mode',
                                            manager=manager, object_id=ObjectID(class_id="@circle_buttons", object_id="#mode_button"))

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
            
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == playButton:
                print("playing")
        manager.process_events(event)
        

    manager.update(time_delta)

    interface.blit(background, (0, 0)) #draw designs after this line

   # pygame.draw.rect(interface, "#999999ff", (0, 0, 180, 600)) #side panel
    pygame.draw.rect(interface, "black", (290, 50, 480, 360)) #temporary display screen 
    pygame.draw.rect(interface, "#d9d9d9ff", (290, 410, 480, 50), 0, 15) #play, stop button bars
    
    
    
    manager.draw_ui(interface)
    pygame.display.update()
    
    
    
# class Button:
#     def __init__(self):
#         self.isClicked = False
#         self.color = (180,180,180)
#     def draw(self):
#         rect()
#     def 
# class dragAndDrop:
#     def __init__(self):
#         self.isClicked = False
#         self.color = (180,180,180)
#     def draw(self):
#         rect()
#     def 
        