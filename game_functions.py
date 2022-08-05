import pygame
from SLTile import SLTile
from SLBrigade import SLBrigade

def move_occupant(origin: SLTile, dest: SLTile, screen):
    # Moves occupant from one tile to another and renders the new scene
    # Parameters: origin - SLTile, the origin of the occupant
    #             dest - SLTile, the destination of the occupant
    #             screen - the game screen

    screen.blit(origin.pygame_surface, origin.top_left_corner)
    dest.occupant = origin.occupant
    origin.occupant = None
    dest.occupant.location = dest
    screen.blit(dest.occupant.pygame_surface, dest.top_left_corner)

def swap_occupants(tile1: SLTile, tile2: SLTile, screen):
    # Swaps occupants between two tiles
    # Parameters: tile1 - SLTile, the active tile
    #             tile2 - SLTile, the selected tile
    #             screen - the game screen

    screen.blit(tile1.pygame_surface, tile1.top_left_corner)
    screen.blit(tile2.pygame_surface, tile2.top_left_corner)
    temp = tile2.occupant
    tile2.occupant = tile1.occupant
    tile1.occupant = temp
    tile1.occupant.location = tile1
    tile2.occupant.location = tile2
    screen.blit(tile1.occupant.pygame_surface, tile1.top_left_corner)
    screen.blit(tile2.occupant.pygame_surface, tile2.top_left_corner)

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
