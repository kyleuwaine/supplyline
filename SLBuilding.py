import enum
import pygame
from enum import Enum
import SLFaction
import SLTile

class SLBuilding:
    # Represents a building which can be placed by players or start on the map.

    class Type(Enum):
        # Represents the type of building. Different types have different abilities.

        CAPITOL = 0
        BARRACKS = 1
    
    def __init__(self, building_type, faction: SLFaction, location: SLTile):
        # Creates a new building
        # Parameters: self - the building object
        #             building_type - the type of building
        #             faction - SLFaction, the faction the building belongs to
        #             location - SLTile, the tile where the building is located

        match building_type:
            case SLBuilding.Type.CAPITOL:
                pass
            case SLBuilding.Type.BARRACKS:
                pass

        self.faction = faction
        self.location = location