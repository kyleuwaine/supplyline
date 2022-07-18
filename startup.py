import pygame
from copy import deepcopy
from SLTile import SLTile

def find_topleft(screen_width, screen_height, hex_sprite_width, hex_sprite_height, grid_width, grid_height):
    assert grid_width % 2 != 0, "expected odd grid width"
    assert grid_height % 2 != 0, "expected even grid height"
    assert grid_height == grid_width, "expected grid height and grid width to be equal"
    x = (screen_width // 2) - (hex_sprite_width // 2)
    y = (screen_height // 2) - (hex_sprite_height // 2) 
    top = x - (hex_sprite_width * (grid_width // 2)), y - (105 * (grid_height // 2))  
    return top
    

def prepare_map(screen, screen_width, screen_height, full_screen_mask_input):
    hex_sprite_width = 120
    hex_sprite_height = 140
    tile_grid_width = 3
    tile_grid_height = 3
    x, y = find_topleft(screen_width, screen_height, hex_sprite_width, hex_sprite_height, tile_grid_width, tile_grid_height)
    tile_grid = [[0 for x in range(tile_grid_width)] for y in range(tile_grid_height)]
    #tile_grid[0][0] = SLTile((0, 0))
    #tile_grid[0][0] = SLTile(( (screen_width // 2) - (hex_sprite_width // 2) , (screen_height // 2) - (hex_sprite_height // 2) ), full_screen_mask_input)
    is_offset = False
    offset = hex_sprite_width // 2
    for i in range(tile_grid_width):
        current_x = x                                                 
        for j in range(tile_grid_height):
            if (is_offset):
                tile_grid[i][j] = SLTile((current_x + offset, y), full_screen_mask_input)
            else: 
                tile_grid[i][j] = SLTile((current_x, y), full_screen_mask_input)

            current_x += hex_sprite_width
            screen.blit(tile_grid[i][j].pygame_surface, tile_grid[i][j].top_left_corner)

        if (is_offset):
            is_offset = False
        else: 
            is_offset = True

        y += 105

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