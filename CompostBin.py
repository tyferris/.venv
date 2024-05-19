import pygame
import sys

class Animation:
    def __init__(self, frames, pos, frame_delay):
        self.frames = frames
        self.pos = pos
        self.frame_delay = frame_delay  # Milliseconds between frames
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.done = False

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.current_frame = 0
                self.done = True

    def draw(self, screen):
        if not self.done:
            screen.blit(self.frames[self.current_frame], self.pos)

# Starts the game
pygame.init()
pygame.display.set_caption('Post.com')
clock = pygame.time.Clock()
animation_delay_ms = 1000

# Screen bounds
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Initialize game objects here
active_item = None
items = []  # x, y, width, height
item_positions = [(890, 35), (890, 149), (890, 262), (890, 376), (890, 490)]

# Load custom images and resize them
item_images = []
for i in range(1, 6):
    img = pygame.image.load(f"object-{i}.png").convert_alpha()
    img = pygame.transform.scale(img, (75, 75))  # Resize to match original rectangle size
    item_images.append(img)

bag_animation_images = []
for i in range(21, 24):
    img = pygame.image.load(f"bague-{i}.png").convert_alpha()
    img = pygame.transform.scale(img, (75, 75))  # Resize to match original rectangle size
    bag_animation_images.append(img)

# Create Rect objects for items and store initial positions
initial_item_positions = []
for i, pos in enumerate(item_positions):
    item_rect = item_images[i].get_rect(topleft=pos)
    items.append(item_rect)
    initial_item_positions.append(pos)  # Store the initial positions

# Background image
image_background = pygame.image.load("backgroundwithpanel-01.png")

# Function to draw the background
def draw_background(image):
    size = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(size, (0, 0))

# List to keep track of animations
animations = []

# Game Loop
run = True
while run:
    clock.tick(60)  # Set to 60 FPS

    draw_background(image_background)

    # Introduce game objects in game here
    for item in items:
        screen.blit(item_images[items.index(item)], item)

    # Update and draw animations
    for animation in animations:
        animation.update()
        animation.draw(screen)
    
    # Remove finished animations
    animations = [anim for anim in animations if not anim.done]

    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                for num, item in enumerate(items):
                    if item.collidepoint(event.pos):
                        active_item = num  # If click on item, it is active.

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if active_item is not None and active_item == 2:  # Specific check for item 3 (index 2)
                    pos = items[active_item].topleft
                    # Reset item to its initial position
                    items[active_item].topleft = initial_item_positions[active_item]
                    # Add a new animation
                    animations.append(Animation(bag_animation_images, pos, animation_delay_ms))  # ms delay between frames
                active_item = None  # No more click, no more active

        if event.type == pygame.MOUSEMOTION:  # If mouse moves...
            if active_item is not None:
                items[active_item].move_ip(event.rel)  # Active item follows it

        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

# Close the game
pygame.quit()
sys.exit()
