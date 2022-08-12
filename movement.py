import pygame
from SLTile import SLTile
from SLBrigade import SLBrigade
from SLFaction import SLFaction

# Contains all game functions related to movement of units

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

def claim_tile(claimed: SLTile, grid):
    # 