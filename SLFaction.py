import pygame

class SLFaction:
    def __init__(self, new_name: str, new_id: int, new_color: pygame.Color, new_brigade_dict: list):
        self.name = new_name
        self.id = new_id
        self.color = new_color
        self.brigade_dict = new_brigade_dict
        self.brigade_counter = 0
        self.building_counter = 0
