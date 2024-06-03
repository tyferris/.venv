import pygame
import MusicScamp
import sys

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
ANIMATION_DELAY_MS = 400
OFFSET_X = -800  # Move 800 pixels to the left
OFFSET_Y = -175  # Move 175 pixels up

class Animation:
    def __init__(self, frames, pos, frame_delay):
        self.frames = frames
        self.pos = pos
        self.frame_delay = frame_delay
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.done = False

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.done = True

    def draw(self, screen):
        if not self.done:
            screen.blit(self.frames[self.current_frame], self.pos)

def draw_background(screen, image):
    size = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(size, (0, 0))

def load_images(image_paths, size):
    images = []
    for path in image_paths:
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, size)
        images.append(img)
    return images

def initialize_items(item_images, positions):
    items = []
    for i, pos in enumerate(positions):
        item_rect = item_images[i].get_rect(topleft=pos)
        items.append(item_rect)
    return items

def main():
    pygame.init()
    pygame.display.set_caption('Post.com')
    clock = pygame.time.Clock()

    # Screen setup
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Load sounds
    MusicScamp.s.fork(MusicScamp.bass_inf, args=[50])

    # Load images
    item_image_paths = [f"object_files/object-{i}.png" for i in range(1, 6)]
    item_images = load_images(item_image_paths, (90, 105))

    bag_animation_image_paths = [f"plasticbaggrain_files/plasticbaggrain_{i}.png" for i in range(1, 65)]
    bag_animation_images = load_images(bag_animation_image_paths, (1402, 546))

    # Initialize game objects
    item_positions = [(1000, 35), (1000, 149), (1000, 262), (1000, 376), (1000, 490)]
    items = initialize_items(item_images, item_positions)

    initial_item_positions = item_positions.copy()

    # Load background
    image_background = pygame.image.load("background_files/background_right.png")

    # List to keep track of animations
    animations = []

    # Store the last dropped position
    last_dropped_position = None

    # Game loop
    run = True
    active_item = None

    while run:
        clock.tick(60)
        draw_background(screen, image_background)

        for item in items:
            screen.blit(item_images[items.index(item)], item)

        for animation in animations:
            animation.update()
            animation.draw(screen)

        animations = [anim for anim in animations if not anim.done]

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for num, item in enumerate(items):
                        if item.collidepoint(event.pos):
                            active_item = num

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and active_item is not None:
                    if active_item == 2:
                        pos = items[active_item].topleft
                        items[active_item].topleft = initial_item_positions[active_item]
                        last_dropped_position = pos
                        item_center = items[active_item].center
                        animation_pos = (
                            item_center[0] + OFFSET_X,
                            item_center[1] + OFFSET_Y
                        )
                        print(f"Item center: {item_center}, Animation pos: {animation_pos}")  # Debug print
                        animations.append(Animation(bag_animation_images, animation_pos, ANIMATION_DELAY_MS))
                    active_item = None

            if event.type == pygame.MOUSEMOTION:
                if active_item is not None:
                    items[active_item].move_ip(event.rel)

            if event.type == pygame.QUIT:
                run = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
