import pygame
import random

# Initialize pygame and create a window
pygame.init()
size = (800, 800)
screen = pygame.display.set_mode(size)

# Load background image
background_image = pygame.image.load("background.png")

# Create the bird character
bird_image = pygame.image.load("bird.png")
bird_image = pygame.transform.scale(bird_image, (50, 50))
bird_rect = bird_image.get_rect()
bird_rect.x = 50
bird_rect.y = 250

# Set gravity variable
gravity = 1

# Set speed variable for the bird moving forward
speed = 15

# Create a list to store the pipes
pipes = []


# Create a function to generate new pipes
def create_pipe():
    pipe_image = pygame.image.load("pipe.jpg")
    pipe_rect = pipe_image.get_rect()
    pipe_rect.x = 150
    pipe_rect.y = random.randint(0, 500)
    pipes.append([pipe_image, pipe_rect])


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # User input to make the bird jump
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        bird_rect.y -= 25

    # Apply gravity to the bird
    bird_rect.y += gravity

    # Move the bird forward
    bird_rect.x += 0

    # Generate new pipes
    if len(pipes) == 0 or pipes[-1][1].x < 0:
        create_pipe()

    # Move the pipes to the left
    for pipe in pipes:
        pipe[1].x -= speed

    # Draw background, bird and pipes on the screen
    screen.blit(background_image, (0, 0))
    screen.blit(bird_image, bird_rect)
    for pipe in pipes:
        screen.blit(pipe[0], pipe[1])
    pygame.display.flip()

# Quit pygame
pygame.quit()