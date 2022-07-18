import pygame
from SLTile import SLTile

def prepare_map(screen, screen_width, screen_height, full_screen_mask_input):
    hex_sprite_width = 120
    hex_sprite_height = 140
    tile_grid_width = 1
    tile_grid_height = 1
    tile_grid = [[0 for x in range(tile_grid_width)] for y in range(tile_grid_height)]
    #tile_grid[0][0] = SLTile((0, 0))
    tile_grid[0][0] = SLTile(( (screen_width // 2) - (hex_sprite_width // 2) , (screen_height // 2) - (hex_sprite_height // 2) ), full_screen_mask_input)
    for i in tile_grid:
        for j in i:
            screen.blit(j.pygame_surface, j.top_left_corner)
    
    return tile_grid


def startup():
    screen_width = 800
    screen_height = 400
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Supply Line")
    clock = pygame.time.Clock()
    framerate = 10
    full_screen_surface = pygame.Surface((screen_width, screen_height))
    full_screen_mask = pygame.mask.from_surface(full_screen_surface)
    full_screen_mask.invert()
    tile_grid = prepare_map(screen, screen_width, screen_height, full_screen_mask)

    return clock, framerate, screen, tile_grid