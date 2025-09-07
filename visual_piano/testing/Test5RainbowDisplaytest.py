# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")


    keys = pygame.key.get_pressed()
    # if keys[pygame.K_q]:
    #     screen.fill("red")
    # if keys[pygame.K_w]:
    #     screen.fill("orange")
    # if keys[pygame.K_e]:
    #     screen.fill("yellow")
    # if keys[pygame.K_r]:
    #     screen.fill("green")
    # if keys[pygame.K_t]:
    #     screen.fill("blue")
    # if keys[pygame.K_y]:
    #     screen.fill("purple")
    if keys[pygame.K_q]:
        screen.fill((0,40,0))
    if keys[pygame.K_w]:
        screen.fill((0,80,0))
    if keys[pygame.K_e]:
        screen.fill((0,120,0))
    if keys[pygame.K_r]:
        screen.fill((0,160,0))
    if keys[pygame.K_t]:
        screen.fill((0,200,0))
    if keys[pygame.K_y]:
        screen.fill((0,255,0))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()