import pygame
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
    hex_sprite_width += 1  # Create a black border between the tiles
    tile_grid_width = 5
    tile_grid_height = 5
    tile_grid_size = 5
    x, y = find_topleft(screen_width, screen_height, hex_sprite_width, hex_sprite_height, tile_grid_width, tile_grid_height)
    tile_grid = [[0 for x in range(tile_grid_width)] for y in range(tile_grid_height)]
    #tile_grid[0][0] = SLTile((0, 0))
    #tile_grid[0][0] = SLTile(( (screen_width // 2) - (hex_sprite_width // 2) , (screen_height // 2) - (hex_sprite_height // 2) ), full_screen_mask_input)
    is_offset = True # Need offset on every other row to properly create a hex map 
    is_skip_last_hex = True
    offset = hex_sprite_width // 2
    for i in range(tile_grid_width): # Loop to fill out tile_grid and render all tiles onto screen
        current_x = x
        for j in range(tile_grid_height):
            if (j == (tile_grid_height - 1)):
                if (is_skip_last_hex == True):
                    tile_grid[i] = tile_grid[i][:-1]
                    is_skip_last_hex = False
                    break
                else:
                    is_skip_last_hex = True
            if (is_offset): 
                if ((j == 0) or (j == tile_grid_width - 2)):
                    tile_grid[i][j] = SLTile((current_x + offset, y), full_screen_mask_input.copy(), SLTile.Type.BORDER)
                elif ((i == 0) or (i == tile_grid_height - 1)):
                    tile_grid[i][j] = SLTile((current_x + offset, y), full_screen_mask_input.copy(), SLTile.Type.BORDER)
                else:
                    tile_grid[i][j] = SLTile((current_x + offset, y), full_screen_mask_input.copy(), SLTile.Type.STANDARD)
            else:
                if ((j == 0) or (j == tile_grid_width - 1)):
                    tile_grid[i][j] = SLTile((current_x, y), full_screen_mask_input.copy(), SLTile.Type.BORDER)
                elif ((i == 0) or (i == tile_grid_height - 1)):
                    tile_grid[i][j] = SLTile((current_x, y), full_screen_mask_input.copy(), SLTile.Type.BORDER)
                else:
                    tile_grid[i][j] = SLTile((current_x, y), full_screen_mask_input.copy(), SLTile.Type.STANDARD)

            current_x += hex_sprite_width
            screen.blit(tile_grid[i][j].pygame_surface, tile_grid[i][j].top_left_corner)

        if (is_offset):
            is_offset = False
        else:
            is_offset = True

        y += 105

    return tile_grid, tile_grid_size


def startup():
    screen_width = 1200
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Supply Line")
    clock = pygame.time.Clock()
    framerate = 10
    full_screen_surface = pygame.Surface((screen_width, screen_height))
    full_screen_mask = pygame.mask.from_surface(full_screen_surface)
    full_screen_mask.invert()
    tile_grid, tile_grid_size = prepare_map(screen, screen_width, screen_height, full_screen_mask)

    return clock, framerate, screen, tile_grid, tile_grid_size
