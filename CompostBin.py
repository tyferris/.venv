import random
import pygame

# Starts the game
pygame.init()

# Screen bounds
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Initialize game objects here
active_item = None
items = []       # x,  y, width, height
item1 = pygame.Rect(890, 35, 75, 75)
item2 = pygame.Rect(890, 149, 75, 75)
item3 = pygame.Rect(890, 262, 75, 75)
item4 = pygame.Rect(890, 376, 75, 75)
item5 = pygame.Rect(890, 490, 75, 75)
items.append(item1)
items.append(item2)
items.append(item3)
items.append(item4)
items.append(item5)

image = pygame.image.load("backgroundwithpanel-01.png")
def Background(image):
    size = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(size, (0, 0))

# Game Loop
run = True
while run:

    # Super important, colors over past frames
    screen.fill("black")

    Background(image)       # lemme commit

    # Introduce game objects in game here
    for item in items:
        pygame.draw.rect(screen, "blue", item)

    # Event Handler
    # Add controls here
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for num, item in enumerate(items):
                    if item.collidepoint(event.pos):
                        active_item = num

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button ==1:
                active_item = None

        if event.type == pygame.MOUSEMOTION:
            if active_item != None:
                items[active_item].move_ip(event.rel)

        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

# Close the game
pygame.quit()