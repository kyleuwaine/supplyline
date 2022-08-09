import pygame

class SLButton:

    def compute_mask(self, full_screen_mask):
        button_mask = pygame.mask.from_surface(self.pygame_surface)
        full_screen_mask.draw(button_mask, self.top_left_corner)
        return full_screen_mask

    def __init__(self, top_left_corner, full_screen_mask, sprite):
        self.top_left_corner = top_left_corner
        self.pygame_surface = pygame.image.load(sprite)
        self.pygame_mask = self.compute_mask(full_screen_mask)

    # Might do this later, but even though rectangular buttons would probably be
    # slightly more performant, they're also uglier than with rounded corners
    #def __init__(self, top_left_corner, full_screen_mask, rect_details, text):
    #    self.top_left_corner = top_left_corner
    #    self.pygame_surface =
    #    self.pygame_surface = pygame.image.load(sprite)
    #    self.pygame_mask = self.compute_mask(full_screen_mask)
