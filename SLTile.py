import pygame

class SLTile:
    def compute_mask(self, full_screen_mask):
        hex_mask = pygame.mask.from_surface(self.pygame_surface)
        full_screen_mask.draw(hex_mask, self.top_left_corner)
        return full_screen_mask

    def __init__(self, top_left_corner, full_screen_mask):
        self.sprite = "Images\grass_05.png"
        self.occupant = None
        self.top_left_corner = top_left_corner
        self.pygame_surface = pygame.image.load(self.sprite)
        self.pygame_mask = self.compute_mask(full_screen_mask)
