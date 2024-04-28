import pygame
import random

from player import *


WIDTH = 800
HEIGHT = 800
FPS = 30

# Define Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

## initialize pygame and create window
pygame.init()
#pygame.mixer.init()  ## For sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Atac")
clock = pygame.time.Clock()     ## For syncing the FPS


## group all the sprites together for ease of update
all_sprites = pygame.sprite.Group()

p1 = Player((0,0), 50, 50, (50, 255, 5),[pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN])
p2 = Player((WIDTH/2, HEIGHT/2), 50, 50, (50, 120, 255), [pygame.K_a, pygame.K_w, pygame.K_d, pygame.K_s])

all_sprites.add(p1)
all_sprites.add(p2)

## Game loop
running = True
ticks_from_previous_iteration = 0
while running:


    #1 Process input/events
    clock.tick(FPS)     ## will make the loop run at the same speed all the time
    events = pygame.event.get()
    for event in events:        # gets all the events which have occured till now and keeps tab of them.
        ## listening for the the X button at the top
        if event.type == pygame.QUIT:
            running = False


    #2 Update

    t = pygame.time.get_ticks()
    # deltaTime in seconds.
    delta_time = (t - ticks_from_previous_iteration ) / 1000.0
    ticks_from_previous_iteration = t

    all_sprites.update(delta_time)


    #3 Draw/render
    screen.fill(BLACK)



    

    all_sprites.draw(screen)
    ########################

    ### Your code comes here

    ########################

    ## Done after drawing everything to the screen
    pygame.display.flip()       

pygame.quit()
