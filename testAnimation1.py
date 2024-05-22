import pygame
from pygame.locals import *
import testSpritesheet # for animation file

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Trash')

sprite_sheet_img = pygame.image.load('testObj.png').convert_alpha()
sprite_sheet = testSpritesheet.SpriteSheet(sprite_sheet_img)

BG = (50,50,50)
BLACK = (0,0,0)

# create animation list
animation_list = []
animation_step = 4
last_update = pygame.time.get_ticks()
animation_cooldown = 500 #fps
frame = 0

for x in range(animation_step):
    animation_list.append(sprite_sheet.get_image(x,24,24,3, BLACK))

# frame_0 = sprite_sheet.get_image(0,24,24,3, BLACK)
# frame_1 = sprite_sheet.get_image(1,24,24,3, BLACK)
# frame_2 = sprite_sheet.get_image(2,24,24,3, BLACK)
# frame_3 = sprite_sheet.get_image(3,24,24,3, BLACK)

run = True
while run:
    #update background(BG)
    screen.fill(BG)
    #update animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(animation_list):
            frame = 0
    #show frame img
    screen.blit(animation_list[frame], (0, 0))
    # for x in range(animation_step):
    #     screen.blit(animation_list[x], (x * 72 , 0))
    # screen.blit(frame_0, (0,0))
    # screen.blit(frame_1, (72,0))
    # screen.blit(frame_2, (150,0))
    # screen.blit(frame_3, (,0))