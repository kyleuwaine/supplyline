import pygame
from enum import Enum
import SLFaction
import SLTile

class SLBrigade:
# Represents a unit that can be moved between hexes and do battle with other
# units and buildings.
# Errors:   AssertionError - If, on initialization, the string does not correlate
#           with a value of the BrigadeType Enum

    class BrigadeType(Enum):
        # Represents the archetype of the unit. Different archetypes have
        # different attack, defense, and movement values.

        TANK = 0

    def __init__(self, brigade_type: str, faction: SLFaction, location: SLTile, id):
        # Creates a new brigade.
        # Parameters: brigade_type - String, will be used to assign the
        #             correct enum for the brigade type
        #             faction - SLFaction, used to check if the current
        #             player can give orders to the brigade
        #             location - SLTile, the tile where the brigade is placed
        #             id = the key used to access the brigade in the faction dictionary

        match brigade_type:
            case "Tank":
                self.type = SLBrigade.BrigadeType.TANK
                self.sprite = "Images\ight_arrow.png"
            case _:
                assert 0 == 1, "Invalid Brigade Type"
        self.health = 100
        self.faction = faction
        self.id = id
        # location is the tile it is currently on
        self.location = location
        self.pygame_surface = pygame.image.load(self.sprite)
