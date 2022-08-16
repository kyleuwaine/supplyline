import pygame
from SLTile import SLTile
from SLBrigade import SLBrigade
from SLFaction import SLFaction
import game_functions
import movement

def battle(attacker: SLBrigade, defender: SLBrigade, grid, screen):
    # Will commence a battle between two brigades on the map
    # Parameters: attacker - SLBrigade, the attacking brigade
    #             defender - SLBrigade, the defending brigade
    #             screen - the screen of the game

    attacker_alive = True
    defender_alive = True
    attacker.health = attacker.health - 15
    defender.health = defender.health - 10
    screen.blit(attacker.location.pygame_surface, attacker.location.top_left_corner)
    screen.blit(attacker.pygame_surface, attacker.location.top_left_corner)
    game_functions.blit_borders(attacker.location, attacker.location.owner.color, screen)
    game_functions.blit_health(attacker, screen)
    screen.blit(defender.location.pygame_surface, defender.location.top_left_corner)
    screen.blit(defender.pygame_surface, defender.location.top_left_corner)
    game_functions.blit_borders(defender.location, defender.location.owner.color, screen)
    game_functions.blit_health(defender, screen)
    if (attacker.health <= 0):
        screen.blit(attacker.location.pygame_surface, attacker.location.top_left_corner)
        game_functions.blit_borders(attacker.location, attacker.location.owner.color, screen)
        attacker.location.occupant = None
        attacker.faction.brigade_dict.pop(attacker.id)
        attacker_alive = False
    if (defender.health <= 0):
        screen.blit(defender.location.pygame_surface, defender.location.top_left_corner)
        game_functions.blit_borders(defender.location, defender.location.owner.color, screen)
        defender.location.occupant = None
        defender.faction.brigade_dict.pop(defender.id)
        defender_alive = False
    if (attacker_alive and not defender_alive):
        movement.move_occupant(attacker.location, defender.location, screen, grid)
        game_functions.blit_borders(defender.location, defender.location.owner.color, screen)
        for tile in (game_functions.find_neighbors(defender.location, grid) + defender.location):
            game_functions.blit_borders(tile, tile.owner.color, screen)
