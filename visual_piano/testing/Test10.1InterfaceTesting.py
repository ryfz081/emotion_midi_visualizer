import pygame
import sys
    
pygame.init()

class Button:
    def __init__(self, color, x, y, width, height, shape, text='', font_size = 12): #shape is a string
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.shape = shape
        self.text = text
        self.font_size = font_size
        self.pressed = False
        self.releaseMode = False

    def draw(self, screen):
        if self.shape == "RECTANGLE":
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        elif self.shape == "ELLIPSE":
            pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.width, self.height))
            
        if self.text != '':
            font = pygame.font.SysFont('comicsans', self.font_size)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def update(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if not self.releaseMode:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if self.isOver((mouse_x, mouse_y)) and self.color == "Blue":
                        self.pressed = True
                        # NewButton.color = "Red"
                    elif self.isOver((mouse_x, mouse_y)):
                        self.pressed = False
                        # NewButton.color = "Blue"
            
            if self.pressed and event.type == pygame.MOUSEBUTTONUP:
                self.color = "Red"
            if not self.pressed and event.type == pygame.MOUSEBUTTONUP:
                self.color = "Blue"
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if self.isOver((mouse_x, mouse_y)) and self.color == "Blue":
                        self.pressed = True
                        # NewButton.color = "Red"
                    elif self.isOver((mouse_x, mouse_y)):
                        self.pressed = False
                        # NewButton.color = "Blue"
 
    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False
    
class DraggableButton(Button):
    def __init__(self, color, x, y, width, height, shape, text='', font_size=12):
        super().__init__(color, x, y, width, height, shape, text, font_size)
        self.dragging = False
        self.original_x = x 
        self.original_y = y
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.lock = True

    def start_drag(self, mouse_x, mouse_y):
        self.original_x = self.x
        self.original_y = self.y
        
        self.dragging = True
        self.drag_offset_x = mouse_x - self.x
        self.drag_offset_y = mouse_y - self.y

    def end_drag(self):
        self.dragging = False
        if self.lock:
            self.x = self.original_x
            self.y = self.original_y

    def drag(self, new_x, new_y):
        if self.dragging:
            self.x = new_x - self.drag_offset_x
            self.y = new_y - self.drag_offset_y
            
    def update(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.drag(mouse_x, mouse_y)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if self.isOver((mouse_x, mouse_y)) and self.color == "Blue":
                    self.pressed = True
                    self.start_drag(mouse_x, mouse_y)
                    self.color = "Red"
                    print("dragging")
                elif self.isOver((mouse_x, mouse_y)):
                    self.pressed = False
                    self.start_drag(mouse_x, mouse_y)
                    self.color = "Red"
                    print("stopped dragging")
        
        if self.pressed and event.type == pygame.MOUSEBUTTONUP:
            self.end_drag()
            self.color = "Blue"
        if not self.pressed and event.type == pygame.MOUSEBUTTONUP:
            self.end_drag()
            self.color = "Blue"


# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 255, 255)
RECTANGLE_COLOR = "Blue"


# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Main game loop
running = True

NewButton = Button("Blue", 10, 10, 50,50, "ELLIPSE", "NEW")
NewDragButton = DraggableButton("Blue", 100, 10, 50, 50, "ELLIPSE", "NEWDRA")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if NewButton.pressed:
                NewDragButton.lock = True
            else:
                NewDragButton.lock = False
    NewButton.update(event)
    NewDragButton.update(event)
    
    
    screen.fill(BACKGROUND_COLOR)
    NewButton.draw(screen)
    NewDragButton.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()