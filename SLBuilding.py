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
        FARM = 4
        OILWELL = 5

        def __str__(input):
            if (input == SLBuilding.Type.CAPITAL):
                return "Capital"
            elif (input == SLBuilding.Type.BARRACKS):
                return "Barracks"
            elif (input == SLBuilding.Type.MINE):
                return "Mine"
            elif (input == SLBuilding.Type.FORT):
                return "Fort"
            elif (input == SLBuilding.Type.FARM):
                return "Farm"
            elif (input == SLBuilding.Type.OILWELL):
                return "Oilwell"
            return None


    class Resource(Enum):
        # Represents the type of resource produced at the building.

        NONE = 0
        METALS = 1
        FOOD = 2
        FUEL = 3


    def __init__(self, building_type, faction: SLFaction, location: SLTile, id: int):
        # Creates a new building
        # Parameters: self - the building object
        #             building_type - the type of building
        #             faction - SLFaction, the faction the building belongs to
        #             location - SLTile, the tile where the building is located
        #             id - the key used to access the created building in the faction dictionary

        if (type(building_type) is str):
            if (building_type == "Capital"):
                building_type = SLBuilding.Type.CAPITAL
            elif (building_type == "Barracks"):
                building_type = SLBuilding.Type.BARRACKS
            elif (building_type == "Mine"):
                building_type = SLBuilding.Type.MINE
            elif (building_type == "Fort"):
                building_type = SLBuilding.Type.FORT
            elif (building_type == "Farm"):
                building_type = SLBuilding.Type.FARM
            elif (building_type == "Oilwell"):
                building_type = SLBuilding.Type.OILWELL

        match building_type:
            case SLBuilding.Type.CAPITAL:
                self.health = 500
                self.force_limit = 0
                self.sprite = base_game_functions.get_selective_image_str("Images/_capital.png", location.map_setting_str)
                self.off_dmg = 0
                self.def_dmg = 30
                self.production = 0
                self.resource = SLBuilding.Resource.NONE
                self.cost = None
            case SLBuilding.Type.BARRACKS:
                self.health = 100
                self.force_limit = 3
                self.sprite = base_game_functions.get_selective_image_str("Images/_barracks.png", location.map_setting_str)
                self.off_dmg = 0
                self.def_dmg = 0
                self.production = 0
                self.resource = SLBuilding.Resource.NONE
                self.cost = 5
            case SLBuilding.Type.MINE:
                self.health = 100
                self.force_limit = 0
                self.sprite = base_game_functions.get_selective_image_str("Images/_mine.png", location.map_setting_str)
                self.off_dmg = 0
                self.def_dmg = 0
                self.production = 5
                self.resource = SLBuilding.Resource.METALS
                self.cost = None
            case SLBuilding.Type.FORT:
                self.health = 300
                self.force_limit = 0
                self.sprite = base_game_functions.get_selective_image_str("Images/_fort.png", location.map_setting_str)
                self.off_dmg = 0
                self.def_dmg = 20
                self.production = 0
                self.resource = SLBuilding.Resource.NONE
                self.cost = 5
            case SLBuilding.Type.FARM:
                self.health = 100
                self.force_limit = 0
                self.sprite = base_game_functions.get_selective_image_str("Images/_farm.png", location.map_setting_str)
                self.off_dmg = 0
                self.def_dmg = 0
                self.production = 5
                self.resource = SLBuilding.Resource.FOOD
                self.cost = None
            case SLBuilding.Type.OILWELL:
                self.health = 100
                self.force_limit = 0
                self.sprite = base_game_functions.get_selective_image_str("Images/_oilwell.png", location.map_setting_str)
                self.off_dmg = 0
                self.def_dmg = 0
                self.production = 5
                self.resource = SLBuilding.Resource.FUEL
                self.cost = None

        self.type = building_type
        # Yes, we do need this, because appearently if (type(tile_grid[i][j].occupant == SLBrigade)) returns true if the occupant is a building...
        self.is_building = True
        self.faction = faction
        self.location = location
        self.id = id
        self.pygame_surface = pygame.image.load(self.sprite)

    def __str__(self):
        return f"{self.is_building}. {str(self.type)}. {self.health}. {self.faction}. {self.location.location}. {self.id}"
