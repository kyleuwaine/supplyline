import pygame
import base_game_functions
from SLTile import SLTile
from SLBrigade import SLBrigade

#def get_selective_image_str(base_image_str):
#    if (screen.get_size() == (1200, 600)):
#        return base_image_str
#    if (screen.get_size() == (1800, 900)):
#        return base_image_str[:-4] + "_half.png"

#def selective_blit(screen, base_image_str, top_left_corner):
#    if (screen.get_size() == (1200, 600)):
#        screen.blit(pygame.image.load(base_image_str), top_left_corner)
#    if (screen.get_size() == (1800, 900)):
#        real_image_str = base_image_str[:-4] + "_half.png"
#        screen.blit(pygame.image.load(real_image_str), top_left_corner)

def blit_borders(tile: SLTile, color, screen):
    #c_red = pygame.Color("red")
    #c_blue = pygame.Color("blue")
    if (color == pygame.Color("red")):
        border_image = base_game_functions.get_selective_image_str("Images\ed_hex_borders.png", screen.get_size())
    elif (color == pygame.Color("blue")):
        border_image = base_game_functions.get_selective_image_str("Images\eblue_hex_borders.png", screen.get_size())
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
