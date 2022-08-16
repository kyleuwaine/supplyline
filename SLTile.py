import pygame
from enum import Enum
import base_game_functions

class SLTile:
    class Type(Enum):
        STANDARD = 1
        BORDER = 2

    def compute_mask(self, full_screen_mask):
        hex_mask = pygame.mask.from_surface(self.pygame_surface)
        full_screen_mask.draw(hex_mask, self.top_left_corner)
        return full_screen_mask

    def __init__(self, top_left_corner, full_screen_mask, tile_type, location, screen_dims):
        if (tile_type == SLTile.Type.STANDARD):
            self.sprite = base_game_functions.get_selective_image_str("Images\grass_05.png", screen_dims)
        elif (tile_type == SLTile.Type.BORDER):
            self.sprite = base_game_functions.get_selective_image_str("Images\dirt_06.png", screen_dims)
        self.type = tile_type
        self.occupant = None
        self.top_left_corner = top_left_corner
        self.pygame_surface = pygame.image.load(self.sprite)
        self.pygame_mask = self.compute_mask(full_screen_mask)
        self.location = location
        self.owner = None
        self.screen_dims = screen_dims
