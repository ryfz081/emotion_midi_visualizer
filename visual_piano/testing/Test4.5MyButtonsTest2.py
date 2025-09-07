import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# Define bounds
min_x, min_y = 80, 80
max_x = 720 - 80
max_y = 720 - 80

kick = pygame.mixer.Sound("analog_kick.wav")
snare = pygame.mixer.Sound("analog_snare.wav")
hihat = pygame.mixer.Sound("analog_closedhat.wav")

class Button:
    def __init__(self, x, y, radius, key, sound):
        self.position = pygame.Vector2(x, y)
        self.radius = radius
        self.original_radius = radius  # Store the original radius
        self.key = key
        self.sound = sound
        self.is_pressed = False

    def draw(self, color):
        pygame.draw.circle(screen, color if self.is_pressed else "blue", self.position, self.radius)

    def increase_radius(self):
        self.radius = 80

    def reset_radius(self):
        self.radius = self.original_radius

# Create three buttons with associated sounds
button_q = Button(160, 360, 40, 'q', kick)
button_w = Button(360, 360, 40, 'w', snare)
button_e = Button(560, 360, 40, 'e', hihat)

buttons = [button_q, button_w, button_e]

# Sound queue
sound_queue = []

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    distance = pygame.Vector2(mouse_pos[0] - button.position.x, mouse_pos[1] - button.position.y).length()
                    if distance <= button.radius:
                        button.is_pressed = True
                        sound_queue.append(button.sound)
                        button.increase_radius()  # Increase radius
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for button in buttons:
                    if button.is_pressed:
                        button.is_pressed = False
                        if button.sound in sound_queue:
                            sound_queue.remove(button.sound)
                        button.reset_radius()  # Reset radius
        if event.type == pygame.KEYDOWN:
            for button in buttons:
                if event.unicode == button.key:
                    button.is_pressed = True
                    sound_queue.append(button.sound)
                    button.increase_radius()  # Increase radius
        if event.type == pygame.KEYUP:
            for button in buttons:
                if event.unicode == button.key:
                    if button.is_pressed:
                        button.is_pressed = False
                        if button.sound in sound_queue:
                            sound_queue.remove(button.sound)
                        button.reset_radius()  # Reset radius

    # fill the screen with a color to wipe away anything from the last frame
    screen.fill("purple")

    # Draw buttons
    buttons[0].draw("black")
    buttons[1].draw("white")
    buttons[2].draw("yellow")

    # Play sounds from the queue
    if sound_queue:
        sound = sound_queue.pop(0)
        sound.play()

    # flip() the display to put your work on the screen
    pygame.display.flip()

    # limits FPS to 60
    dt = clock.tick(60) / 1000

pygame.quit()
