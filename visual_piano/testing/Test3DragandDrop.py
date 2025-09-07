import pygame
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 255, 255)
RECTANGLE_COLOR = "Blue"

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drag and Drop in Pygame")

# Rectangle properties
rect_width, rect_height = 100, 100
rect_x, rect_y = 100, 100
dragging = False

# Define bounds
min_x, min_y = 0, 0
max_x = WIDTH - rect_width
max_y = HEIGHT - rect_height

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                print(event.pos)
                print((rect_x, rect_x+rect_width), (rect_y, rect_y + rect_height))
                if rect_x < event.pos[0] and event.pos[0] < rect_x + rect_width and rect_y < event.pos[1] and event.pos[1] < rect_y + rect_height:
                    dragging = True
                    offset_x = event.pos[0] - rect_x
                    offset_y = event.pos[1] - rect_y
            

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
                RECTANGLE_COLOR = "Blue"

    if dragging:
        RECTANGLE_COLOR = "Red"
        print("bro")
        rect_x, rect_y = pygame.mouse.get_pos()
        rect_x -= offset_x
        rect_y -= offset_y

        # Bound checking
        if rect_x < min_x:
            rect_x = min_x
        elif rect_x > max_x:
            rect_x = max_x
        if rect_y < min_y:
            rect_y = min_y
        elif rect_y > max_y:
            rect_y = max_y

    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, RECTANGLE_COLOR, (rect_x, rect_y, rect_width, rect_height))

    pygame.display.flip()

pygame.quit()
sys.exit()
