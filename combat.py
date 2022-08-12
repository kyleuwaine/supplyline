import pygame
from SLTile import SLTile
from SLBrigade import SLBrigade
from SLFaction import SLFaction
import game_functions
import movement

def battle(attacker: SLBrigade, defender: SLBrigade, screen):
    # Will commence a battle between two brigades on the map
    # Parameters: attacker - SLBrigade, the attacking brigade
    #             defender - SLBrigade, the defending brigade
    #             screen - the screen of the game

    attacker_alive = True
    defender_alive = True
    attacker.health = attacker.health - 15
    defender.health = defender.health - 10
    if (attacker.health <= 0):
        screen.blit(attacker.location.pygame_surface, attacker.location.top_left_corner)
        attacker.location.occupant = None
        attacker.faction.brigade_list.clear()
        attacker_alive = False
    if (defender.health <= 0):
        screen.blit(defender.location.pygame_surface, defender.location.top_left_corner)
        defender.location.occupant = None
        defender.faction.brigade_list.clear()
        defender_alive = False
    if (attacker_alive and not defender_alive):
        movement.move_occupant(attacker.location, defender.location, screen)