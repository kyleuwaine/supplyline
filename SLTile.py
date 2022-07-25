import pygame
from enum import Enum 

class SLTile:
    class Type(Enum): 
        STANDARD = 1
        BORDER = 2 
    
    def compute_mask(self, full_screen_mask):
        hex_mask = pygame.mask.from_surface(self.pygame_surface)
        full_screen_mask.draw(hex_mask, self.top_left_corner)
        return full_screen_mask

    def __init__(self, top_left_corner, full_screen_mask, tile_type):
        if (tile_type == SLTile.Type.STANDARD): 
            self.sprite = "Images\grass_05.png"
        elif (tile_type == SLTile.Type.BORDER):
            self.sprite = "Images\dirt_06.png"
        self.type = tile_type
        self.occupant = None
        self.top_left_corner = top_left_corner
        self.pygame_surface = pygame.image.load(self.sprite)
        self.pygame_mask = self.compute_mask(full_screen_mask)
