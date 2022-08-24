import game_functions
import SLFaction
import combat
import movement
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

    def AI_turn(self):
        # Performs the AI turn by moving all of its brigades to random empty neighboring tiles

        eliminated_brigades = []

        for id in self.faction.brigade_dict:
            brigade = self.faction.brigade_dict[id]
            original_location = brigade.location
            possible_dests = movement.find_valid_moves(original_location, False, self.map, self.screen)
            selected_dest = possible_dests[randrange(0, len(possible_dests))]
            movement.attempt_move(original_location, selected_dest, possible_dests, self.map, self.screen)

        for brigade in eliminated_brigades:
            game_functions.remove_entity(brigade)
