import pygame
from SLTile import SLTile
from SLBrigade import SLBrigade
from SLFaction import SLFaction
import game_functions
import base_game_functions
import combat

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

def find_valid_moves(origin: SLTile, show_moves: bool, grid, screen):
    # Finds the valid tiles that an entity can move to.
    # Highlights the valid tiles to move to if show_moves == True
    # Parameters: origin - SLTile, the tile which contains the entity
    #             grid - the grid containing the tiles of the map
    #             screen - the screen of the game
    #             show_moves - bool, indicates whether to highlight the valid moves or not
    # Returns a list containing the valid tiles

    if (origin.occupant.moves <= 0):
        return []

    valid_tiles = []
    jumps = []

    if (not origin.occupant.is_building):
        for tile in game_functions.find_neighbors(origin, grid):
            if (origin.occupant.type == SLBrigade.BrigadeType.TANK and tile.type == SLTile.Type.MOUNTAINS):
                continue
            if (tile.occupant == None):
                valid_tiles.append(tile)
            else:
                if (tile.occupant.is_building == False):
                    valid_tiles.append(tile)
                else:
                    if (tile.owner != origin.owner):
                        valid_tiles.append(tile)
                    elif (tile.owner == origin.owner):
                        for jump in game_functions.find_neighbors(tile, grid):
                            jumps.append(jump)
        for jump in jumps:
            if (origin.occupant.type == SLBrigade.BrigadeType.TANK and jump.type == SLTile.Type.MOUNTAINS):
                continue
            if (jump not in valid_tiles and jump != origin):
                if (jump.occupant == None):
                    valid_tiles.append(jump)
                else:
                    if (jump.occupant.is_building == False):
                        valid_tiles.append(jump)
                    else:
                        if (jump.owner != origin.owner):
                            valid_tiles.append(jump)
    
    if (show_moves):
        for tile in valid_tiles:
            screen.blit(pygame.image.load(base_game_functions.get_selective_image_str("Images\_purple_hex.png", tile.map_setting_str)), tile.top_left_corner)
    
    return valid_tiles

def attempt_move(origin: SLTile, dest: SLTile, valid_moves, grid, screen):
    # Attempts to move a brigade from the origin tile to the destination tile.
    # If there are no occupants in the destination, the brigade will simply move to the destination.
    # Otherwise: If the occupant at the destination is of the same faction, they will swap.
    #            If the occupant at the destination is of another faction, a battle will start.
    # Parameters: origin - SLTile, the tile containing the moving brigade
    #             dest - SLTile, the tile being moved to
    #             valid_moves - a list containing the valid tiles that can be moved to
    #             grid - the grid containing the tiles of the map
    #             screen - the screen of the game
    # Returns True if the brigade is moved, and also a list of any entities which get removed in battle

    moved = False
    eliminated = []

    if (dest in valid_moves):
        if (dest.type == SLTile.Type.MOUNTAINS or dest.type == SLTile.Type.JUNGLE):
            origin.occupant.moves = 0
        else:
            origin.occupant.moves -= 1
        if (dest.occupant != None):
        # checks if there is an occupant on the selected tile
            if (dest.occupant.faction == origin.occupant.faction):
            # if the selected tile's occupant is of the same faction as the player, it will swap the two occupants
                swap_occupants(origin, dest, screen)
                moved = True
            else:
            # if the selected tile's occupant is of a different faction, a battle will ensue
                attacker = origin.occupant
                defender = dest.occupant
                result = combat.battle(attacker, defender, grid, screen)
                if (result == 1):
                # defender died
                    eliminated.append(defender)
                elif (result == 2):
                # attacker died
                    eliminated.append(attacker)
                elif (result == 3):
                # both died
                    eliminated.append(attacker)
                    eliminated.append(defender)
                moved = True
        else:
        # if there is no occupant on the selected tile, the highlighted tile's occupant will move to the selected tile
            move_occupant(origin, dest, screen, grid)
            moved = True

    if (moved):
        for tile in valid_moves:
            game_functions.reblit_tile(tile, screen)
    
    return moved, eliminated
        
def reset_moves(brigade: SLBrigade):
    # Resets the available moves of a brigade back to the max amount at the end of a turn
    # Parameters: brigade - SLBrigade, the brigade being reset

    brigade.moves = brigade.max_moves