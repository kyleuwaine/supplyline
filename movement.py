import pygame
from SLTile import SLTile
from SLBrigade import SLBrigade
from SLFaction import SLFaction
import game_functions

# Contains all game functions related to movement of units

def move_occupant(origin: SLTile, dest: SLTile, screen, grid):
    # Moves occupant from one tile to another and renders the new scene
    # Parameters: origin - SLTile, the origin of the occupant
    #             dest - SLTile, the destination of the occupant
    #             screen - the game screen

    dest.occupant = origin.occupant
    origin.occupant = None
    dest.occupant.location = dest
    game_functions.reblit_tile(origin, screen)
    attempt_claim(dest, origin.owner, screen, grid)

def swap_occupants(tile1: SLTile, tile2: SLTile, screen):
    # Swaps occupants between two tiles
    # Parameters: tile1 - SLTile, the active tile
    #             tile2 - SLTile, the selected tile
    #             screen - the game screen

    temp = tile2.occupant
    tile2.occupant = tile1.occupant
    tile1.occupant = temp
    tile1.occupant.location = tile1
    tile2.occupant.location = tile2
    game_functions.reblit_tile(tile1, screen)
    game_functions.reblit_tile(tile2, screen)

def attempt_claim(claimed: SLTile, faction: SLFaction, screen, grid):
    # Attempts to claim a tile and any unclaimed tile which also borders it.
    # Parameters: claimed - SLTile, the tile being claimed
    #             grid - the grid which contains the tiles
    #             faction - SLFaction, the faction attempting to claim the tile

    claimed.owner = faction
    game_functions.reblit_tile(claimed, screen)

    surrounding = game_functions.find_empty_neighbors(claimed, grid)
    for tile in surrounding:
        if (tile.owner == None):
            tile.owner = faction
            game_functions.reblit_tile(tile, screen)
