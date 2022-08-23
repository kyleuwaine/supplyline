import pygame
from SLTile import SLTile
from SLBrigade import SLBrigade
from SLFaction import SLFaction
import game_functions
import movement
from SLBuilding import SLBuilding

def battle(attacker: SLBrigade, defender, grid, screen):
    # Will commence a battle between two entities on the map
    # If defender is type == SLBrigade, battle_brigade() is called
    # If defender is type == SLBuilding, battle_building() is called
    # Parameters: attacker - SLBrigade, the attacking brigade
    #             defender - the defending entity
    #             grid - the grid containing the game tiles
    #             screen - the screen of the game
    # Returns an int indicating the result of the battle (in terms of surviving brigades)
    # Return Values: 0 - Both attacker and defender survived
    #                1 - Attacker survived and defender eliminated
    #                2 - Attacker eliminated and defender survived
    #                3 - Both attacker and defender eliminated

    if (type(defender) == SLBrigade):
        return battle_brigade(attacker, defender, grid, screen)
    elif (type(defender) == SLBuilding):
        return battle_building(attacker, defender, grid, screen)


def battle_brigade(attacker: SLBrigade, defender: SLBrigade, grid, screen):
    # Will commence a battle between two brigades on the map
    # For each brigade of the attacker's faction that borders the defender, the attacker does 5 more damage.
    # Same rule for support applies to defender.
    # Parameters: attacker - SLBrigade, the attacking brigade
    #             defender - SLBrigade, the defending brigade
    #             grid - the grid containing the game tiles
    #             screen - the screen of the game
    # Returns an int indicating the result of the battle (in terms of surviving brigades)
    # Return Values: 0 - Both attacker and defender survived
    #                1 - Attacker survived and defender eliminated
    #                2 - Attacker eliminated and defender survived
    #                3 - Both attacker and defender eliminated

    attacker_alive = True
    defender_alive = True

    # Calculating total support damage for both brigades
    att_sup = 0 # the amount of damage that the attacker will do from support
    def_sup = 0 # the amount of damage that the defender will do from support
    for tile in game_functions.find_neighbors(defender.location, grid):
    # Searching neighbors of defender to find brigades which support the attacker
        if (tile.occupant.faction == attacker.faction and tile.occupant != attacker):
            if (type(tile.occupant) == SLBrigade):
                att_sup += 5
    for tile in game_functions.find_neighbors(attacker.location, grid):
    # Searching neighbors of attacker to find brigades which support the defender
        if (tile.occupant.faction == defender.faction and tile.occupant != defender):
            if (type(tile.occupant) == SLBrigade):
                def_sup += 5

    # Calculating total damage attacker does
    total_att_dmg = attacker.off_dmg + att_sup
    # Calculating total damage defender does
    total_def_dmg = defender.def_dmg + def_sup

    # Dealing damage to brigades
    attacker.health = attacker.health - total_def_dmg
    defender.health = defender.health - total_att_dmg

    # Re-rendering screen to properly show the change in health of brigades
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


def battle_building(attacker: SLBrigade, defender: SLBuilding, grid, screen):
    # Will commence a battle between a brigade and building on the map
    # Parameters: attacker - SLBrigade, the attacking brigade
    #             defender - SLBuilding, the defending brigade
    #             grid - the grid containing the game tiles
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
