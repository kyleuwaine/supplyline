import pygame
from enum import Enum
import base_game_functions

class SLTile:
    class Type(Enum):
        STANDARD = 1
        BORDER = 2
        MOUNTAINS = 3
        HILLS = 4
        JUNGLE = 5

        def __str__(input):
            if (input == SLTile.Type.STANDARD):
                return "Standard"
            if (input == SLTile.Type.BORDER):
                return "Border"
            if (input == SLTile.Type.MOUNTAINS):
                return "Mountains"
            if (input == SLTile.Type.HILLS):
                return "Hills"
            if (input == SLTile.Type.STANDARD):
                return "Standard"
            return None

    def compute_mask(self, full_screen_mask):
        # Computes the mask of a tile
        # Parameters: full_screen_mask - the mask of the whole game screen, onto which the tile's mask is drawn
        # Returns the mask of the tile

        hex_mask = pygame.mask.from_surface(self.pygame_surface)
        full_screen_mask.draw(hex_mask, self.top_left_corner)
        return full_screen_mask

    def __init__(self, top_left_corner, full_screen_mask, tile_type, location, map_setting_str):
        # Initializes the tile object
        # Parameters: top_left_corner - the top left corner of the texture, from where to render the tile onto the screen
        #             full_screen_mask - the mask of the full game screen
        #             tile_type - the type of tile that is being initialized
        #             location - the location of the tile on the map (a grid), stored as a tuple of indices
        #             map_setting_str - a string which contains info about the map

        self.type = tile_type
        self.occupant = None
        self.top_left_corner = top_left_corner
        self.location = location
        self.map_setting_str = map_setting_str
        if (type(tile_type) is str):
            if (tile_type == "Standard"):
                self.change_type(SLTile.Type.STANDARD)
            elif (tile_type == "Border"):
                self.change_type(SLTile.Type.BORDER)
            elif (tile_type == "Mountains"):
                self.change_type(SLTile.Type.MOUNTAINS)
            elif (tile_type == "Hills"):
                self.change_type(SLTile.Type.HILLS)
            elif (tile_type == "Jungle"):
                self.change_type(SLTile.Type.JUNGLE)
            else:
                assert(0 == 1)
        else:
            if (tile_type == SLTile.Type.STANDARD):
                self.sprite = base_game_functions.get_selective_image_str("Images\grass_05.png", map_setting_str)
            elif (tile_type == SLTile.Type.BORDER):
                self.sprite = base_game_functions.get_selective_image_str("Images\dirt_06.png", map_setting_str)
        self.pygame_surface = pygame.image.load(self.sprite)
        self.pygame_mask = self.compute_mask(full_screen_mask)
        self.owner = None

    def change_type(self, new_type):
        # Changes the tile type of a tile
        # Parameters: self - the tile being changed
        #             new_type - the new tile type
        #             screen_dims = the dimensions of the screen of the game

        self.type = new_type

        if (new_type == SLTile.Type.STANDARD):
            self.sprite = base_game_functions.get_selective_image_str("Images\_plains.png", self.map_setting_str)
        elif (new_type == SLTile.Type.BORDER):
            self.sprite = base_game_functions.get_selective_image_str("Images\dirt_06.png", self.map_setting_str)
        elif (new_type == SLTile.Type.MOUNTAINS):
            self.sprite = base_game_functions.get_selective_image_str("Images\_mountain.png", self.map_setting_str)
        elif (new_type == SLTile.Type.HILLS):
            self.sprite = base_game_functions.get_selective_image_str("Images\_hills.png", self.map_setting_str)
        elif (new_type == SLTile.Type.JUNGLE):
            self.sprite = base_game_functions.get_selective_image_str("Images\_jungle.png", self.map_setting_str)

    def __str__(self):
        return f"{str(self.type)}. {self.top_left_corner}. {self.location}. {self.owner}. {self.map_setting_str}. {str(self.occupant)}"
