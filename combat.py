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
        if (tile.occupant != None and tile.occupant != attacker):
            if (tile.owner == attacker.faction):
                if (not tile.occupant.is_building):
                    att_sup += 5
                elif (tile.occupant.type == SLBuilding.Type.FORT):
                    att_sup += 5
    for tile in game_functions.find_neighbors(attacker.location, grid):
    # Searching neighbors of attacker to find brigades which support the defender
        if (tile.occupant != None and tile.occupant != defender):
            if (tile.owner == attacker.faction):
                if (not tile.occupant.is_building):
                    def_sup += 5
                elif (tile.occupant.type == SLBuilding.Type.FORT):
                    def_sup += 5

    # Calculating total damage attacker does
    total_att_dmg = attacker.off_dmg + att_sup
    # Calculating total damage defender does
    total_def_dmg = defender.def_dmg + def_sup + defender.location.defense

    # Dealing damage to brigades
    attacker.health = attacker.health - total_def_dmg
    defender.health = defender.health - total_att_dmg

    if (attacker.health <= 0):
        attacker.location.occupant = None
        attacker_alive = False
    if (defender.health <= 0):
        defender.location.occupant = None
        defender_alive = False

    # Reblitting tiles to show change in brigade healths and if any brigades died
    game_functions.reblit_tile(attacker.location, screen)
    game_functions.reblit_tile(defender.location, screen)

    if (attacker_alive and not defender_alive):
        movement.move_occupant(attacker.location, defender.location, screen, grid)
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
    
    # Calculating total support damage for both brigades
    att_sup = 0 # the amount of damage that the attacker will do from support
    def_sup = 0 # the amount of damage that the defender will do from support
    for tile in game_functions.find_neighbors(defender.location, grid):
    # Searching neighbors of defender to find brigades which support the attacker
        if (tile.occupant != None and tile.occupant != attacker):
            if (tile.owner == attacker.faction):
                if (not tile.occupant.is_building):
                    att_sup += 5
    for tile in game_functions.find_neighbors(attacker.location, grid):
    # Searching neighbors of attacker to find brigades which support the defender
        if (tile.occupant != None and tile.occupant != defender):
            if (tile.owner == attacker.faction):
                if (not tile.occupant.is_building):
                    def_sup += 5
                elif (tile.occupant.type == SLBuilding.Type.FORT):
                    def_sup += 5

    # Calculating total damage attacker does
    total_att_dmg = attacker.off_dmg + att_sup
    # Calculating total damage defender does
    total_def_dmg = defender.def_dmg + def_sup + defender.location.defense

    # Dealing damage to brigades
    attacker.health = attacker.health - total_def_dmg
    defender.health = defender.health - total_att_dmg

    if (attacker.health <= 0):
        attacker.location.occupant = None
        attacker_alive = False
    if (defender.health <= 0):
        if (not defender.production > 0):
            defender.location.occupant = None
        defender_alive = False

    # Reblitting tiles to show change in brigade healths and if any brigades died
    game_functions.reblit_tile(attacker.location, screen)
    game_functions.reblit_tile(defender.location, screen)

    if (attacker_alive and not defender_alive):
        if (not defender.production > 0):
            movement.move_occupant(attacker.location, defender.location, screen, grid)
            return 1
        else: 
            defender.faction = attacker.faction
            defender.location.owner = attacker.faction
            game_functions.reblit_tile(defender.location, screen)
            for tile in game_functions.find_empty_neighbors(defender.location, grid):
                if (tile.owner == None):
                    tile.owner = attacker.faction
                    game_functions.reblit_tile(tile, screen)
            return 0
    elif (attacker_alive and defender_alive):
        return 0
    elif (not attacker_alive and defender_alive):
        return 2
    elif (not attacker_alive and not defender_alive):
        if (not defender.production > 0):
            return 3
        else:
            return 2