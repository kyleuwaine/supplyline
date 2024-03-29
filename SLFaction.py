"""
This file contains the class SLFaction, which holds all of the variables pertaining to a specific faction,
as well as the non-static function rec_capability(), which calculates if a specific factions should be able
to build additional tank and infantry brigades or not.

Author: Kyle Uwaine and Victor Nault
Date: 10/12/22
"""

import pygame

class SLFaction:
    # Represents a faction within the game

    def __init__(self, new_name: str, new_id: int, new_color: pygame.Color, new_brigade_dict: dict, new_building_dict: dict):
        # Intializes a faction
        # Parameters: new_name - str, the name of the faction
        #             new_id - int, the id of the faction
        #             new_color - pygame.Color, the color of the faction
        #             new_brigade_dict - list, the dict containing the brigades this faction controls

        self.name = new_name
        self.id = new_id
        self.color = new_color
        self.brigade_dict = new_brigade_dict
        self.building_dict = new_building_dict
        self.brigade_id_counter = 0
        self.building_id_counter = 0
        self.brigade_cap = 3
        self.brigade_counter = 1
        self.metals = 5
        self.food = 5
        self.fuel = 0
        self.capital_loc = None
        self.is_defeated = False


    def rec_capability(self):
        # Calculates the recruitment capability of this faction
        # Returns: below_cap - True if amount of brigades currently owned is below the brigade cap
        #          can_recruit_infantry - True if faction has enough resources to recruit infantry
        #          can_recruit_tank - True if faction has enough resources to recruit tanks

        below_cap = False
        if (self.metals >= 5):
            can_recruit_infantry = True
            can_recruit_tank = True
        else:
            can_recruit_infantry = False
            can_recruit_tank = False
            
        # Note: brigade counter isn't actually incremented anywhere else in the code, so this snippet is useless
        # Fixing it isn't really in scope for the current iteration of the project, so I'm disabling it for now
        #if (self.brigade_cap > self.brigade_counter):
            #below_cap = True
        below_cap = True

        return below_cap, can_recruit_infantry, can_recruit_tank

    def __str__(self):
        return f"Faction {self.id}"
