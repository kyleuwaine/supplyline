import enum
import pygame
from enum import Enum
import SLFaction
import SLTile

class SLBuilding:
    # Represents a building which can be placed by players or start on the map.

    class Type(Enum):
        # Represents the type of building. Different types have different abilities.

        CAPITAL = 0
        BARRACKS = 1
        MINE = 2
    
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
                self.force_limit = 5
            case SLBuilding.Type.BARRACKS:
                self.health = 100
                self.force_limit = 3
            case SLBuilding.Type.MINE:
                self.health = 100
                self.force_limit = 0

        self.faction = faction
        self.location = location
        self.id = id