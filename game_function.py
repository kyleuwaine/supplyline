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

def advance_turn(faction_turn: int, num_of_players: int):
    faction_turn += 1
    faction_turn = faction_turn % num_of_players
    return faction_turn
