import pygame
import rtmidi
import sys
def main():
    # Initialize pygame
    pygame.init()
    midiin = rtmidi.MidiIn()
    ports = range(midiin.get_port_count())

    # Constants
    SCREEN_WIDTH = 1760
    SCREEN_HEIGHT = 600
    BAR_COLOR = (0, 128, 255)
    BAR_WIDTH = 20
    BAR_MAX_HEIGHT = 600  # Maximum height of the bar
    BAR_SPEED = 12

    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Expanding Bar")

    # Bar position and size
    bar_x = SCREEN_WIDTH // 2 - BAR_WIDTH // 2
    bar_bottom_y = SCREEN_HEIGHT  # Start at the bottom of the screen
    bar_height = 0

    # Flags
    expanding = False

    # Main game loop
    running = True
    clock = pygame.time.Clock()

    if ports: #if midi has port
        midiin.open_port(0)
        while running:
            m = midiin.get_message()
            if m:
                # print(m)
                if is_Note(m):
                    if is_On(m):
                        expanding = True
                    else:
                        expanding = False
                else: #pedal
                    if is_On(m):
                        expanding = True
                    else:
                        expanding = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
           
                # elif event.type == pygame.MOUSEBUTTONDOWN:
                #     if event.button == 1:  # Left mouse button
                #         expanding = True
                # elif event.type == pygame.MOUSEBUTTONUP:
                #     if event.button == 1:
                #         expanding = False

            # Process mouse button holding
            if expanding and bar_height < BAR_MAX_HEIGHT:
                # Expand the bar upwards while the left mouse button is held
                bar_height += BAR_SPEED
            elif not expanding and bar_height > 0:
                # Shrink the bar back down when the left mouse button is released
                bar_height -= BAR_SPEED * 7

            # Clear the screen
            screen.fill((0, 0, 0))

            # Draw the bar
            pygame.draw.rect(screen, BAR_COLOR, (bar_x, bar_bottom_y - bar_height, BAR_WIDTH, bar_height))

            # Update the display
            pygame.display.flip()

            # Limit the frame rate
            clock.tick(60)
    else:
        print("No Ports Found!")
    # Quit the game
    pygame.quit()
    sys.exit()

def is_Note(message):
    return message[0][0] == 144

def is_On(message):
    return message[0][2] != 0

main()
