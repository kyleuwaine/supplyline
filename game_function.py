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
    screen.blit(tile1.occupant.pygame_surface, tile1.top_left_corner)
    screen.blit(tile2.occupant.pygame_surface, tile2.top_left_corner)

def advance_turn(faction_turn: int, num_of_players: int):
    faction_turn += 1
    faction_turn = faction_turn % num_of_players
    return faction_turn
