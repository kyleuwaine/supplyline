import enum
import pygame
from enum import Enum
import SLFaction
import SLTile
import base_game_functions
import game_functions

class SLBuilding:
    # Represents a building which can be placed by players or start on the map.

    class Type(Enum):
        # Represents the type of building. Different types have different abilities.

        CAPITAL = 0
        BARRACKS = 1
        MINE = 2
        FORT = 3

    def __init__(self, building_type, faction: SLFaction, location: SLTile, id):
        # Creates a new building
        # Parameters: self - the building object
        #             building_type - the type of building
        #             faction - SLFaction, the faction the building belongs to
        #             location - SLTile, the tile where the building is located
        #             id - the key used to access the created building in the faction dictionary

        match building_type:
            case SLBuilding.Type.CAPITAL:
                self.health = 500
                self.force_limit = 0
                self.sprite = base_game_functions.get_selective_image_str("Images\_capital.png", location.map_setting_str)
                self.off_dmg = 0
                self.def_dmg = 30
            case SLBuilding.Type.BARRACKS:
                self.health = 100
                self.force_limit = 3
                self.sprite = base_game_functions.get_selective_image_str("Images\_barracks.png", location.map_setting_str)
                self.off_dmg = 0
                self.def_dmg = 0
            case SLBuilding.Type.MINE:
                self.health = 100
                self.force_limit = 0
                self.sprite = base_game_functions.get_selective_image_str("Images\_mine.png", location.map_setting_str)
                self.off_dmg = 0
                self.def_dmg = 0
            case SLBuilding.Type.FORT:
                self.health = 300
                self.force_limit = 0
                self.sprite = base_game_functions.get_selective_image_str("Images\_mine.png", location.map_setting_str)
                self.off_dmg = 0
                self.def_dmg = 20

        self.type = building_type
        # Yes, we do need this, because appearently if (type(tile_grid[i][j].occupant == SLBrigade)) returns true if the occupant is a building...
        self.is_building = True
        self.faction = faction
        self.location = location
        self.id = id
        self.pygame_surface = pygame.image.load(self.sprite)
