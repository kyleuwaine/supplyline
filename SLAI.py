import game_functions
from SLFaction import *
from SLBuilding import *
from SLBrigade import *
import combat
import movement
from turn_crunch import turn_crunch
from random import randrange

class SLAI:
    # Represents an AI opponent
    # Parameters:   faction - the faction that the AI controls
    #               map - the hex grid the game is being played on
    #               screen - the pygame screen

    def __init__(self, faction: SLFaction, map, screen):
        self.faction = faction
        self.map = map
        self.screen = screen

    """
    def AI_turn(self):
        # Performs the AI turn by moving all of its brigades to random empty neighboring tiles

        eliminated_brigades = []

        for id in self.faction.brigade_dict:
            brigade = self.faction.brigade_dict[id]
            while (brigade.moves > 0):
                original_location = brigade.location
                possible_dests = movement.find_valid_moves(original_location, False, self.map, self.screen)
                selected_dest = possible_dests[randrange(0, len(possible_dests))]
                moved, eliminated = movement.attempt_move(original_location, selected_dest, possible_dests, self.map, self.screen)
                for entity in eliminated:
                    eliminated_brigades.append(entity)

        for brigade in eliminated_brigades:
            game_functions.remove_entity(brigade)

        turn_crunch(self.faction, self.map, len(self.map), self.screen)
    """

    def AI_turn(self):
            for row in self.map:
                for tile in row:
                    if (tile.owner != self.faction):
                            continue
                    rand_int = randrange(100)
                    if (tile.occupant == None):
                        if (self.faction.metals >= 5):
                                if (rand_int < 3):
                                    game_functions.build_building(SLBuilding.Type.BARRACKS, tile, self.faction, self.screen, False)
                                elif (rand_int < 7):
                                    game_functions.build_building(SLBuilding.Type.FORT, tile, self.faction, self.screen, False)
                    elif(tile.occupant.is_building == True):
                        if (rand_int < 10):
                            if(self.faction.metals >= 5):
                                if(tile.occupant.type == (SLBuilding.Type.BARRACKS or SLBuilding.Type.CAPITAL)):
                                    valid_rec_locs = game_functions.find_valid_rec_locs(tile, self.map)
                                    if (valid_rec_locs != []):
                                        selected_loc = valid_rec_locs[randrange(len(valid_rec_locs))]
                                        if (rand_int < 5):
                                            game_functions.build_brigade("Tank", selected_loc, self.faction, self.screen, False)
                                        else:
                                            game_functions.build_brigade("Infantry", selected_loc, self.faction, self.screen, False)
                    else:
                        if (rand_int < 5):
                            continue
                        eliminated_brigades = []
                        moving_brigade = tile.occupant
                        while ((moving_brigade.moves > 0) and (moving_brigade.health > 0)):
                            original_location = moving_brigade.location
                            possible_dests = movement.find_valid_moves(original_location, False, self.map, None)
                            if (possible_dests != []):
                                selected_dest = possible_dests[randrange(0, len(possible_dests))]
                                moved, eliminated = movement.attempt_move(original_location, selected_dest, possible_dests, self.map, self.screen)
                                for entity in eliminated:
                                    eliminated_brigades.append(entity)
                            else:
                                break
                        for brigade in eliminated_brigades:
                            game_functions.remove_entity(brigade)

            turn_crunch(self.faction, self.map, len(self.map), self.screen)
