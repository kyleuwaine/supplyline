import pygame

# This one is for game functions that do not require any imports except pygame

def get_selective_image_str(base_image_str: str, map_setting_str: str):
    if (map_setting_str == "big_tiles_debug_map"):
        return base_image_str
    if (map_setting_str == "small_tiles_std_map"):
        return base_image_str[:-4] + "_half.png"

def advance_turn(faction_turn: int, num_of_players: int):
    # Advances the turn of the game and gives control to the next faction
    # Parameters: faction_turn - int, an int which represents which faction is currently active
    #             num_of_players - int, the amount of players in the game

    faction_turn += 1
    faction_turn = faction_turn % num_of_players
    return faction_turn

#def selective_blit(screen, base_image_str, top_left_corner):
#    if (screen.get_size() == (1200, 600)):
#        screen.blit(pygame.image.load(base_image_str), top_left_corner)
#    if (screen.get_size() == (1800, 900)):
#        real_image_str = base_image_str[:-4] + "_half.png"
#        screen.blit(pygame.image.load(real_image_str), top_left_corner)
