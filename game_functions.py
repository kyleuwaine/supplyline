import pygame
import base_game_functions
import json
import os
from SLTile import SLTile
from SLBrigade import SLBrigade
from SLBuilding import SLBuilding
from SLFaction import SLFaction

def export_map(hex_grid, hex_grid_size: int):
    hex_str_grid = [[None for x in range(hex_grid_size)] for y in range(hex_grid_size)]
    for i in range(len(hex_grid)):
        for j in range(len(hex_grid[i])):
            print(str(hex_grid[i][j]))
            hex_str_grid[i][j] = str(hex_grid[i][j])

    if os.path.exists("custom_map.json"):
        os.remove("custom_map.json")
    with open("custom_map.json", "w") as output:
        json.dump(hex_str_grid, output, indent = 4)

#wip
def import_map(full_screen_mask_input):
    with open("custom_map.json", "r") as input:
        input_lst = json.load(input)
    tile_str_lst = []
    for i in range(len(input_lst)):
        tile_str_lst.append([])
        for j in range(len(input_lst[i])):
            #print(input_lst[i][j])
            if(input_lst[i][j] != None):
                tile_str_lst[i].append(input_lst[i][j].split(". "))
            else:
                tile_str_lst[i].append(None)
    map_setting_str = tile_str_lst[0][0][4]
    hex_sprite_width, hex_sprite_height, tile_grid_width, tile_grid_height, tile_grid_size, vertical_offset = base_game_functions.set_map_settings(map_setting_str)
    hex_grid = [[0 for x in range(tile_grid_width)] for y in range(tile_grid_height)]
    for i in range(tile_grid_width):
        for j in range(tile_grid_height):
            if (tile_str_lst[i][j] != None):
                hex_grid[i][j] = SLTile(eval(tile_str_lst[i][j][1]), full_screen_mask_input.copy(), tile_str_lst[i][j][0], eval(tile_str_lst[i][j][2]), map_setting_str)
    return hex_grid


def find_valid_rec_locs(this_tile: SLTile, grid):
    # Finds all valid locations for recruitment from this building
    # Parameters: grid - the grid containing the tiles on the map
    # Returns the valid locations in a list

    valid_locs = []

    for tile in find_empty_neighbors(this_tile, grid):
        if (tile.owner == this_tile.owner):
            valid_locs.append(tile)

    return valid_locs

def blit_borders(tile: SLTile, color, screen):
    # Blits borders on a tile
    # Parameters: tile - SLTile, the tile whose borders are being blitted
    #             color - the color of the border
    #             screen - the screen of the game

    #c_red = pygame.Color("red")
    #c_blue = pygame.Color("blue")
    if (color == pygame.Color("red")):
        border_image = base_game_functions.get_selective_image_str("Images\ed_hex_borders.png", tile.map_setting_str)
    elif (color == pygame.Color("blue")):
        border_image = base_game_functions.get_selective_image_str("Images\eblue_hex_borders.png", tile.map_setting_str)
    screen.blit(pygame.image.load(border_image), tile.top_left_corner)


def advance_turn(faction_turn: int, num_of_players: int):
    # Advances the turn of the game and gives control to the next faction
    # Parameters: faction_turn - int, an int which represents which faction is currently active
    #             num_of_players - int, the amount of players in the game

    faction_turn += 1
    faction_turn = faction_turn % num_of_players
    return faction_turn

def find_neighbors(origin: SLTile, grid):
    # Finds and returns a list of all valid neighbor tiles (not borders) around the tile passed in
    # Parameters: origin - SLTile, the tile which is being searched
    #             grid - the grid which contains the tiles

    neighbors = []
    y, x = origin.location

    if (y % 2 == 0):
        if (grid[y][x + 1].type != SLTile.Type.BORDER):
            neighbors.append(grid[y][x + 1])
        if (grid[y][x - 1].type != SLTile.Type.BORDER):
            neighbors.append(grid[y][x - 1])
        if (grid[y - 1][x].type != SLTile.Type.BORDER):
            neighbors.append(grid[y - 1][x])
        if (grid[y - 1][x + 1].type != SLTile.Type.BORDER):
            neighbors.append(grid[y - 1][x + 1])
        if (grid[y + 1][x].type != SLTile.Type.BORDER):
            neighbors.append(grid[y + 1][x])
        if (grid[y + 1][x + 1].type != SLTile.Type.BORDER):
            neighbors.append(grid[y + 1][x + 1])
    else:
        if (grid[y][x + 1].type != SLTile.Type.BORDER):
            neighbors.append(grid[y][x + 1])
        if (grid[y][x - 1].type != SLTile.Type.BORDER):
            neighbors.append(grid[y][x - 1])
        if (grid[y - 1][x].type != SLTile.Type.BORDER):
            neighbors.append(grid[y - 1][x])
        if (grid[y - 1][x - 1].type != SLTile.Type.BORDER):
            neighbors.append(grid[y - 1][x - 1])
        if (grid[y + 1][x].type != SLTile.Type.BORDER):
            neighbors.append(grid[y + 1][x])
        if (grid[y + 1][x - 1].type != SLTile.Type.BORDER):
            neighbors.append(grid[y + 1][x - 1])

    return neighbors

def find_empty_neighbors(origin: SLTile, grid):
    # Finds and returns a list of all valid empty neighbor tiles (not borders) around the tile passed in
    # Parameters: origin - SLTile, the tile which is being searched
    #             grid - the grid which contains the tiles

    # Could do this in-place with one list, but prioritizing performance over memory here
    processing_list = find_neighbors(origin, grid)
    output_list = []

    for tile_index in range(len(processing_list)):
        if (processing_list[tile_index].occupant == None):
            output_list.append(processing_list[tile_index])
    return output_list

def blit_health(entity, screen):
    # Blits the health of an entity onto the tile
    # Parameters: brigade - the entity whose health is being blitted
    #             screen - the screen of the game

    map_setting_str = entity.location.map_setting_str
    if (map_setting_str == "big_tiles_debug_map"):
        font = pygame.font.SysFont("arial", 30)
        x, y = entity.location.top_left_corner
        x += 35
        y += 12
    if (map_setting_str == "small_tiles_std_map"):
        font = pygame.font.SysFont("arial", 20)
        x, y = entity.location.top_left_corner
        x += 25
        y += 10
    health_surface = font.render(str(entity.health), None, entity.faction.color)
    screen.blit(health_surface, (x, y))

def remove_entity(entity):
    # Removes an entity from any lists it is present in
    # Parameters: entity - the entity being removed

    if (not entity.is_building):
        entity.faction.brigade_dict.pop(entity.id)
    elif (entity.is_building):
        entity.faction.building_dict.pop(entity.id)


def reblit_tile(tile: SLTile, screen):
    # Reblits a tile and anything on it
    # Used mainly for unhighligting a tile or if any changes occur to a tile
    # Parameters: tile - SLTile, the tile being reblitted
    #             screen - the screen of the game

    screen.blit(tile.pygame_surface, tile.top_left_corner)
    if (tile.owner != None):
        blit_borders(tile, tile.owner.color, screen)
    if (tile.occupant != None):
        screen.blit(tile.occupant.pygame_surface, tile.top_left_corner)
        blit_health(tile.occupant, screen)
