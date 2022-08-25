import pygame

class SLFaction:
    # Represents a faction within the game

    def __init__(self, new_name: str, new_id: int, new_color: pygame.Color, new_brigade_dict: dict):
        # Intializes a faction
        # Parameters: new_name - str, the name of the faction
        #             new_id - int, the id of the faction
        #             new_color - pygame.Color, the color of the faction
        #             new_brigade_dict - list, the dict containing the brigades this faction controls

        self.name = new_name
        self.id = new_id
        self.color = new_color
        self.brigade_dict = new_brigade_dict
        self.brigade_id_counter = 0
        self.building_id_counter = 0
        self.brigade_cap = 3
        self.brigade_counter = 1
        self.metals = 0
        self.food = 5
        self.oil = 0


    def rec_capability(self):
        # Calculates the recruitment capability of this faction
        # Returns: below_cap - True if amount of brigades currently owned is below the brigade cap
        #          can_recruit_infantry - True if faction has enough resources to recruit infantry
        #          can_recruit_tank - True if faction has enough resources to recruit tanks

        below_cap = False
        can_recruit_infantry = True
        can_recruit_tank = True

        if (self.brigade_cap > self.brigade_counter):
            below_cap = True

        return below_cap, can_recruit_infantry, can_recruit_tank

    def __str__(self):
        return f"Faction {self.id}"
