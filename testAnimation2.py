import pygame, sys

# from pygame.sprite import Group

class obj (pygame.sprite.Sprite):
    def __init__(self, pos_x , pos_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('trash11.png')) #single move
        self.sprites.append(pygame.image.load('trash21.png'))
        self.sprites.append(pygame.image.load('trash31.png'))
        self.sprites.append(pygame.image.load('trash41.png'))
        
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        # self.image = pygame.Surface([20,20])
        # self.image.fill((255,255,255))

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x , pos_y]
    def update(self):
        self.current_sprite += 1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

pygame.init()
clock = pygame.time.Clock()

screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("TEST")

moving_sprites = pygame.sprite.Group()
obj1 = obj(100,100)
moving_sprites.add(obj1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0,0,0))
    moving_sprites.draw(screen)
    moving_sprites.update()
    pygame.display.flip()
    clock.tick(1) #FPS