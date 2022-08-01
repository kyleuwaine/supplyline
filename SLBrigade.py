import pygame
from enum import Enum
import SLFaction

class SLBrigade:
"""
Represents a unit that can be moved between hexes and do battle with other
units and buildings.
"""

    class BrigadeType(Enum):
        """
        Represents the archetype of the unit. Different archetypes have
        different attack, defense, and movement values.
        """
        TANK = 0

    def __init__(self, brigade_type: str, faction):
        """
        Creates a new brigade.
        Parameters: brigade_type - String, will be used to assign the
                    correct enum for the brigade type
                    faction - 
        """
        match brigade_type:
            case "Tank":
                self.type = SLBrigade.BrigadeType.TANK
                self.sprite = "Images\ight_arrow.png"
            case _:
                assert 0 == 1, "Invalid Brigade Type"
        self.health = 100
        self.faction = faction
        self.pygame_surface = pygame.image.load(self.sprite)
