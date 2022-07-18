import pygame
from sys import exit
from SLTile import SLTile

def prepare_map(full_screen_mask_input):
    hex_sprite_width = 120
    hex_sprite_height = 140
    tile_grid_width = 1
    tile_grid_height = 1
    global tile_grid
    tile_grid = [[0 for x in range(tile_grid_width)] for y in range(tile_grid_height)]
    #tile_grid[0][0] = SLTile((0, 0))
    tile_grid[0][0] = SLTile(( (screen_width // 2) - (hex_sprite_width // 2) , (screen_height // 2) - (hex_sprite_height // 2) ), full_screen_mask_input)
    for i in tile_grid:
        for j in i:
            screen.blit(j.pygame_surface, j.top_left_corner)

pygame.init()
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Supply Line")
clock = pygame.time.Clock()
framerate = 10
full_screen_surface = pygame.Surface((screen_width, screen_height))
full_screen_mask = pygame.mask.from_surface(full_screen_surface)
full_screen_mask.invert()
prepare_map(full_screen_mask)

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
