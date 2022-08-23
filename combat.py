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
    # Returns an int indicating the result of the battle (in terms of surviving brigades)
    # Return Values: 0 - Both attacker and defender survived
    #                1 - Attacker survived and defender eliminated
    #                2 - Attacker eliminated and defender survived
    #                3 - Both attacker and defender eliminated

    attacker_alive = True
    defender_alive = True
    attacker.health = attacker.health - 15
    defender.health = defender.health - 10
    screen.blit(attacker.location.pygame_surface, attacker.location.top_left_corner)
    screen.blit(attacker.pygame_surface, attacker.location.top_left_corner)
    game_functions.blit_borders(attacker.location, attacker.location.owner.color, screen)
    game_functions.blit_health(attacker, screen, attacker.location.map_setting_str)
    screen.blit(defender.location.pygame_surface, defender.location.top_left_corner)
    screen.blit(defender.pygame_surface, defender.location.top_left_corner)
    game_functions.blit_borders(defender.location, defender.location.owner.color, screen)
    game_functions.blit_health(defender, screen, defender.location.map_setting_str)

    if (attacker.health <= 0):
        screen.blit(attacker.location.pygame_surface, attacker.location.top_left_corner)
        game_functions.blit_borders(attacker.location, attacker.location.owner.color, screen)
        attacker.location.occupant = None
        attacker_alive = False
    if (defender.health <= 0):
        screen.blit(defender.location.pygame_surface, defender.location.top_left_corner)
        game_functions.blit_borders(defender.location, defender.location.owner.color, screen)
        defender.location.occupant = None
        defender_alive = False
    if (attacker_alive and not defender_alive):
        movement.move_occupant(attacker.location, defender.location, screen, grid)
        game_functions.blit_borders(defender.location, defender.location.owner.color, screen)
        for tile in (game_functions.find_empty_neighbors(defender.location, grid)):
            game_functions.blit_borders(tile, tile.owner.color, screen)
        return 1
    elif (attacker_alive and defender_alive):
        return 0
    elif (not attacker_alive and defender_alive):
        return 2
    elif (not attacker_alive and not defender_alive):
        return 3
