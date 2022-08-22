import pygame

# This one is for game functions that do not require any imports except pygame

def get_selective_image_str(base_image_str: str, map_setting_str: str):
    if (map_setting_str == "big_tiles_debug_map"):
        return base_image_str
    if (map_setting_str == "small_tiles_std_map"):
        return base_image_str[:-4] + "_half.png"

#def selective_blit(screen, base_image_str, top_left_corner):
#    if (screen.get_size() == (1200, 600)):
#        screen.blit(pygame.image.load(base_image_str), top_left_corner)
#    if (screen.get_size() == (1800, 900)):
#        real_image_str = base_image_str[:-4] + "_half.png"
#        screen.blit(pygame.image.load(real_image_str), top_left_corner)
