import pygame
import sys

# Starts the game
pygame.init()
FPS = 10
fpsClock = pygame.time.Clock()

# Screen bounds
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Initialize game objects here
active_item = None
items = []       # x,  y, width, height
item_positions = [(890, 35), (890, 149), (890, 262), (890, 376), (890, 490)]

# Load custom images and resize them
item_images = []
for i in range(1, 6):
    img = pygame.image.load(f"object-{i}.png").convert_alpha()
    img = pygame.transform.scale(img, (75, 75))  # Resize to match original rectangle size
    item_images.append(img)

# Create Rect objects for items
for i, pos in enumerate(item_positions):
    item_rect = item_images[i].get_rect(topleft=pos)
    items.append(item_rect)

# background image
image_background = pygame.image.load("backgroundwithpanel-01.png")

# turns the blank background into the selected image
def Background(image):
    size = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(size, (0, 0))

# Game Loop
run = True
while run:

    # Super important, colors over past frames
    #screen.fill("black")

    Background(image_background)

    # Introduce game objects in game here
    for item in items:
        screen.blit(item_images[items.index(item)], item)

    # Event Handler
    # Add controls here
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:   #left mouse button
                for num, item in enumerate(items):
                    if item.collidepoint(event.pos):
                        active_item = num   # If click on item, it active.

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button ==1:
                active_item = None  #no more click, no more active

        if event.type == pygame.MOUSEMOTION:    # If mouse moves...
            if active_item is not None:
                items[active_item].move_ip(event.rel)   #active item follows it

        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

# Close the game
pygame.quit()
