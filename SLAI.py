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
        for brigade in self.faction.brigade_list:
            possible_dests = game_functions.find_neighbors(brigade.location, self.map)
            selected_dest = possible_dests[randrange(0, len(possible_dests))]
            if (selected_dest.occupant == None):
                movement.move_occupant(brigade.location, selected_dest, self.screen, self.map)
                #movement.attempt_claim(selected_dest, self.faction, self.map)
            else:
                if (selected_dest.occupant.faction == self.faction):
                    movement.swap_occupants(brigade.location, selected_dest, self.screen)
                else:
                    success = combat.battle(brigade, selected_dest.occupant, self.screen)
                    if (success):
                        #movement.attempt_claim(selected_dest, self.faction, self.map)
                        pass
