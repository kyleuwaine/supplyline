import pygame

class SLFaction:
    def __init__(self, new_name: str, new_id: int, new_color: pygame.Color, new_brigade_list: list):
        self.name = new_name
        self.id = new_id
        self.color = new_color
        self.brigade_list = new_brigade_list
        self.brigade_counter = 0
        self.building_counter = 0
