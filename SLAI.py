import game_functions
import SLFaction
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
        for brigade in self.faction.brigade_list:
            possible_dests = game_functions.find_empty_neighbors(brigade.location, self.map)
            game_functions.move_occupant(brigade.location, possible_dests[randrange(0, len(possible_dests))], self.screen)
