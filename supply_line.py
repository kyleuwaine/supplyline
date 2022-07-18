import pygame
from sys import exit
from SLTile import SLTile
from startup import startup

pygame.init()
clock, framerate, screen, tile_grid = startup()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i in tile_grid:
                    for j in i:
                        try:
                            if j.pygame_mask.get_at(event.pos) == 1:
                                print("pog")
                            else:
                                print("Not poggers")
                        except IndexError:
                            pass 


    #screen.blit(test_surface, (200, 100))

    pygame.display.update()
    clock.tick(framerate)
