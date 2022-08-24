import pygame
import game_functions
from SLFaction import SLFaction
from SLBrigade import SLBrigade
from SLTile import SLTile
from SLAI import SLAI
from SLButton import SLButton

def create_init_brigades(faction_list: list, tile_grid: list, screen):
    # Creates the starting brigades for factions in the game
    # Parameters: faction_list - list, the list of factions in the game
    #             tile_grid - list, the grid which contains the tiles of the game
    #             screen - the screen of the game

    tile_grid[1][1].occupant = SLBrigade("Tank", faction_list[0], tile_grid[1][1], faction_list[0].brigade_id_counter)
    tile_grid[1][1].owner = faction_list[0]
    game_functions.blit_borders(tile_grid[1][1], tile_grid[1][1].owner.color, screen)
    faction_list[0].brigade_dict.update({faction_list[0].brigade_id_counter: tile_grid[1][1].occupant})
    faction_list[0].brigade_id_counter += 1
    screen.blit(tile_grid[1][1].occupant.pygame_surface, tile_grid[1][1].top_left_corner)
    game_functions.blit_health(tile_grid[1][1].occupant, screen)
    tile_grid[2][2].occupant = SLBrigade("Tank", faction_list[1], tile_grid[2][2], faction_list[1].brigade_id_counter)
    tile_grid[2][2].owner = faction_list[1]
    game_functions.blit_borders(tile_grid[2][2], tile_grid[2][2].owner.color, screen)
    faction_list[1].brigade_dict.update({faction_list[0].brigade_id_counter: tile_grid[2][2].occupant})
    faction_list[1].brigade_id_counter += 1
    screen.blit(tile_grid[2][2].occupant.pygame_surface, tile_grid[2][2].top_left_corner)
    game_functions.blit_health(tile_grid[2][2].occupant, screen)
    tile_grid[1][2].occupant = SLBrigade("Tank", faction_list[1], tile_grid[1][2], faction_list[1].brigade_id_counter)
    tile_grid[1][2].owner = faction_list[1]
    game_functions.blit_borders(tile_grid[1][2], tile_grid[1][2].owner.color, screen)
    faction_list[1].brigade_dict.update({faction_list[1].brigade_id_counter: tile_grid[1][2].occupant})
    faction_list[1].brigade_id_counter += 1
    screen.blit(tile_grid[1][2].occupant.pygame_surface, tile_grid[1][2].top_left_corner)
    game_functions.blit_health(tile_grid[1][2].occupant, screen)

def create_factions(num_of_factions: int, faction_color_list):
    # Creates the factions of a game
    # Parameters: num_of_factions - int, the number of factions in the game
    #             faction_color_list - a list containing the possible colors for factions
    # Returns a list of the factions in the game

    faction_list = []
    for i in range(num_of_factions):
        faction_list.append(SLFaction(None, i, faction_color_list[i], {}))
    return faction_list

def find_topleft(screen_width, screen_height, hex_sprite_width, hex_sprite_height, grid_width, grid_height, vertical_offset):
    # Find the topleft pixel coordinate of the map
    # Parameters: screen_width - the width of the game screen
    #             screen_height - the height of the game screen
    #             hex_sprite_width - the width of the sprites used for tiles
    #             hex_sprite_height - the height of the sprites used for tiles
    #             grid_width - the width of the map (in terms of tiles)
    #             grid_height - the height of the map (in terms of tiles)
    #             vertical_offset - the offset of the map from the edge of the screen
    # Returns the top left corner of the map

    assert grid_width % 2 != 0, "expected odd grid width"
    assert grid_height % 2 != 0, "expected even grid height"
    assert grid_height == grid_width, "expected grid height and grid width to be equal"
    x = (screen_width // 2) - (hex_sprite_width // 2)
    y = (screen_height // 2) - (hex_sprite_height // 2)
    top = x - (hex_sprite_width * (grid_width // 2)), y - (vertical_offset * (grid_height // 2))
    return top

def prepare_map(screen, screen_width, screen_height, full_screen_mask_input, map_setting_str):
    # Prepares the map of the game
    # Parameters: screen - the screen of the game
    #             screen_width - the width of the screen of the game
    #             screen_height - the height of the screen of the game
    #             full_screen_mask_input - a mask of the whole game screen
    #             map_setting_str - a string which contains info about the map (the size)
    # Returns the grid containing the tiles of the game and the grid's size

    hex_sprite_width = 120
    hex_sprite_height = 140
    if (map_setting_str == "big_tiles_debug_map"):
        hex_sprite_width = 120
        hex_sprite_height = 140
        tile_grid_width = 5
        tile_grid_height = 5
        tile_grid_size = 5
        vertical_offset = 105
    if (map_setting_str == "small_tiles_std_map"):
        hex_sprite_width = 85
        hex_sprite_height = 99
        tile_grid_width = 15
        tile_grid_height = 15
        tile_grid_size = 15
        vertical_offset = 73
    #hex_sprite_width += 1  # Create a black border between the tiles

    x, y = find_topleft(screen_width, screen_height, hex_sprite_width, hex_sprite_height, tile_grid_width, tile_grid_height, vertical_offset)
    tile_grid = [[0 for x in range(tile_grid_width)] for y in range(tile_grid_height)]
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
                    tile_grid[i][j] = SLTile((current_x + offset, y), full_screen_mask_input.copy(), SLTile.Type.BORDER, (i, j), map_setting_str)
                elif ((i == 0) or (i == tile_grid_height - 1)):
                    tile_grid[i][j] = SLTile((current_x + offset, y), full_screen_mask_input.copy(), SLTile.Type.BORDER, (i, j), map_setting_str)
                else:
                    tile_grid[i][j] = SLTile((current_x + offset, y), full_screen_mask_input.copy(), SLTile.Type.STANDARD, (i, j), map_setting_str)
            else:
                if ((j == 0) or (j == tile_grid_width - 1)):
                    tile_grid[i][j] = SLTile((current_x, y), full_screen_mask_input.copy(), SLTile.Type.BORDER, (i, j), map_setting_str)
                elif ((i == 0) or (i == tile_grid_height - 1)):
                    tile_grid[i][j] = SLTile((current_x, y), full_screen_mask_input.copy(), SLTile.Type.BORDER, (i, j), map_setting_str)
                else:
                    tile_grid[i][j] = SLTile((current_x, y), full_screen_mask_input.copy(), SLTile.Type.STANDARD, (i, j), map_setting_str)

            current_x += hex_sprite_width
            screen.blit(tile_grid[i][j].pygame_surface, tile_grid[i][j].top_left_corner)

        if (is_offset):
            is_offset = False
        else:
            is_offset = True

        y += vertical_offset

    return tile_grid, tile_grid_size


def startup(clock, framerate, screen, screen_width, screen_height, map_setting_str):
    # Performs all initializations for the game
    # Parameters: clock - the clock of the game
    #             framerate - the framerate for the game
    #             screen - the screen of the game
    #             screen_width - the width of the game screen
    #             screen_height - the height of the game screen
    #             map_setting_str - a string containing info about the map size
    # Returns initialized items and lists, which will be used throughout the game
    
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Supply Line")
    clock = pygame.time.Clock()
    framerate = 10
    full_screen_surface = pygame.Surface((screen_width, screen_height))
    full_screen_mask = pygame.mask.from_surface(full_screen_surface)
    full_screen_mask.invert()
    num_of_factions = 2
    faction_turn = 0
    faction_color_list = [pygame.Color("red"), pygame.Color("blue")]
    faction_list = create_factions(num_of_factions, faction_color_list)
    tile_grid, tile_grid_size = prepare_map(screen, screen_width, screen_height, full_screen_mask, map_setting_str)
    create_init_brigades(faction_list, tile_grid, screen)
    opponent = SLAI(faction_list[1], tile_grid, screen)
    endturn_button = SLButton([20, 20], full_screen_mask.copy(), "Images\endturn.png")
    screen.blit(endturn_button.pygame_surface, endturn_button.top_left_corner)
    buildbuilding_button = SLButton([screen_width - 140, 20], full_screen_mask.copy(), "Images\_buildbuilding_grey.png", "Images\_buildbuilding_green.png")
    screen.blit(buildbuilding_button.pygame_surface, buildbuilding_button.top_left_corner)
    buildunit_button = SLButton([screen_width - 280, 20], full_screen_mask.copy(), "Images\_buildunit_grey.png", "Images\_buildunit_green.png")
    screen.blit(buildunit_button.pygame_surface, buildunit_button.top_left_corner)

    return tile_grid, tile_grid_size, faction_turn, num_of_factions, faction_list, opponent, endturn_button, buildbuilding_button, buildunit_button, screen
