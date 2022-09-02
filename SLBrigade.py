import pygame
from enum import Enum
import SLFaction
import SLTile
import base_game_functions

class SLBrigade:
# Represents a unit that can be moved between hexes and do battle with other
# units and buildings.
# Errors:   AssertionError - If, on initialization, the string does not correlate
#           with a value of the BrigadeType Enum

    class BrigadeType(Enum):
        # Represents the archetype of the unit. Different archetypes have
        # different attack, defense, and movement values.
        TANK = 0
        INFANTRY = 1

        def __str__(input):
            if (input == SLBrigade.BrigadeType.TANK):
                return "Tank"
            if (input == SLBrigade.BrigadeType.INFANTRY):
                return "Infantry"
            return None

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
                self.sprite = base_game_functions.get_selective_image_str("Images\ight_arrow.png", location.map_setting_str)
                self.off_dmg = 20
                self.def_dmg = 15
                self.food_consumption = 0
                self.fuel_consumption = 1
                self.moves = 2
                self.max_moves = 2
            case "Infantry":
                self.type = SLBrigade.BrigadeType.INFANTRY
                self.sprite = base_game_functions.get_selective_image_str("Images\_infantry.png", location.map_setting_str)
                self.off_dmg = 10
                self.def_dmg = 15
                self.food_consumption = 1
                self.fuel_consumption = 0
                self.moves = 1
                self.max_moves = 1
            case _:
                assert 0 == 1, "Invalid Brigade Type"
        self.health = 100
        self.faction = faction
        self.id = id
        # location is the tile it is currently on
        self.location = location
        self.pygame_surface = pygame.image.load(self.sprite)
        # Yes, we do need this, because appearently if (type(tile_grid[i][j].occupant == SLBrigade)) returns true if the occupant is a building...
        self.is_building = False

    def __str__(self):
        return f"{self.is_building}. {str(self.type)}. {self.health}. {self.faction}. {self.location.location}. {self.id}"
