import pygame
import base_game_functions
from SLTile import SLTile
from SLBrigade import SLBrigade
from SLBuilding import SLBuilding
from SLFaction import SLFaction

def blit_borders(tile: SLTile, color, screen):
    #c_red = pygame.Color("red")
    #c_blue = pygame.Color("blue")
    if (color == pygame.Color("red")):
        border_image = base_game_functions.get_selective_image_str("Images\ed_hex_borders.png", tile.map_setting_str)
    elif (color == pygame.Color("blue")):
        border_image = base_game_functions.get_selective_image_str("Images\eblue_hex_borders.png", tile.map_setting_str)
    screen.blit(pygame.image.load(border_image), tile.top_left_corner)


def advance_turn(faction_turn: int, num_of_players: int):
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

def blit_health(brigade: SLBrigade, screen):
    # Blits the health of a brigade onto the tile
    # Parameters: brigade - SLBrigade, the brigade whose health is being blitted
    #             screen - the screen of the game

    if (screen.get_size() == (1200, 600)):
        font = pygame.font.SysFont("arial", 30)
        x, y = brigade.location.top_left_corner
        x += 35
        y += 12
    if (screen.get_size() == (1800, 900)):
        font = pygame.font.SysFont("arial", 20)
        x, y = brigade.location.top_left_corner
        x += 25
        y += 10
    health_surface = font.render(str(brigade.health), None, brigade.faction.color)
    screen.blit(health_surface, (x, y))

def remove_entity(entity):
    # Removes an entity from any lists it is present in
    # Parameters: entity - the entity being removed

    if (type(entity) == SLBrigade):
        entity.faction.brigade_dict.pop(entity.id)
    elif (type(entity) == SLBuilding):
        entity.faction.building_dict.pop(entity.id)
