# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((720,720))
clock = pygame.time.Clock()
running = True
dt = 0

# Define bounds
min_x, min_y = 80, 80
max_x = 720 - 80
max_y = 720 - 80

boom = pygame.mixer.Sound("buzzer.wav")
border = pygame.mixer.Sound("wrong.wav")

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
button_pressed = False
button_sound = True
border_sound = True
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                button_pressed = True
                offset_x = event.pos[0] - player_pos.x
                offset_y = event.pos[1] - player_pos.y

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                button_pressed = False
                button_sound = True
                border_sound = True
                
                

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    if button_pressed:
        if button_sound:
            boom.play(0)
            button_sound = False
        pygame.draw.circle(screen, "red", player_pos, 80)
        player_pos.x, player_pos.y = pygame.mouse.get_pos()
        player_pos.x -= offset_x
        player_pos.y -= offset_y
        
        if player_pos.x < min_x:
            player_pos.x = min_x
            if border_sound:
                border.play(0)
                border_sound = False
        elif player_pos.x > max_x:
            player_pos.x = max_x
            if border_sound:
                border.play(0)
                border_sound = False
        if player_pos.y < min_y:
            player_pos.y = min_y
            if border_sound:
                border.play(0)
                border_sound = False
        elif player_pos.y > max_y:
            player_pos.y = max_y
            if border_sound:
                border.play(0)
                border_sound = False


    else:
        pygame.draw.circle(screen, "red", player_pos, 40)




    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()




