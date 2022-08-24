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

    def compute_mask(self, full_screen_mask):
        hex_mask = pygame.mask.from_surface(self.pygame_surface)
        full_screen_mask.draw(hex_mask, self.top_left_corner)
        return full_screen_mask

    def __init__(self, top_left_corner, full_screen_mask, tile_type, location, map_setting_str):
        if (tile_type == SLTile.Type.STANDARD):
            self.sprite = base_game_functions.get_selective_image_str("Images\grass_05.png", map_setting_str)
        elif (tile_type == SLTile.Type.BORDER):
            self.sprite = base_game_functions.get_selective_image_str("Images\dirt_06.png", map_setting_str)
        self.type = tile_type
        self.occupant = None
        self.top_left_corner = top_left_corner
        self.pygame_surface = pygame.image.load(self.sprite)
        self.pygame_mask = self.compute_mask(full_screen_mask)
        self.location = location
        self.owner = None
        self.map_setting_str = map_setting_str

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
