import game_functions
import SLFaction
from random import randrange

class SLAI:
    def __init__(self, faction: SLFaction, map, screen):
        self.faction = faction
        self.map = map
        self.screen = screen

    def AI_turn(self):
        for brigade in self.faction.brigade_list:
            possible_dests = game_functions.find_empty_neighbors(brigade.location, self.map)
            game_functions.move_occupant(brigade.location, possible_dests[randrange(0, len(possible_dests))], self.screen)
