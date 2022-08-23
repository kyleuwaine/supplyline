import pygame
from sys import exit
from SLTile import SLTile
from SLBrigade import SLBrigade
from startup import startup
from SLButton import SLButton
import game_functions
import base_game_functions
import combat
import movement

"""
This file contains the main function for the Supplyline program, as well as other
functions that are needed to handle the main event loop. main() first
creates a launcher that contains options for game settings, then calls
menu_screen_loop(), which acts as the event loop until the game is started by
indicating an appropriate option. After the game is started, main() acts as the
event loop for the Supplyline program.

Author: Kyle Uwaine and Victor Nault
Date: 8/20/2022
"""


def menu_screen_loop(small_screen_button: SLButton, big_screen_button: SLButton, clock, framerate: int):
    """
    Is the event loop for the launcher.
    """
    while True:
        #start_game = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (small_screen_button.pygame_mask.get_at(event.pos) == 1):
                        small_screen_button.pygame_mask.clear()
                        big_screen_button.pygame_mask.clear()
                        return 1366, 768, "big_tiles_debug_map"
                        #start_game = True
                    if (big_screen_button.pygame_mask.get_at(event.pos) == 1):
                        small_screen_button.pygame_mask.clear()
                        big_screen_button.pygame_mask.clear()
                        return 1920, 1080, "small_tiles_std_map"

        pygame.display.update()
        clock.tick(framerate)

def main():
    """
    Initializes the launcher, then calls menu_screen_loop(). After menu_screen_loop()
    returns what the user indicates they want the game options to be, initializes
    the main Supplyline program and then acts as the event loop for it.
    """
    pygame.init()
    screen_width = 400
    screen_height = 200
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Supply Line")
    clock = pygame.time.Clock()
    framerate = 10
    full_screen_surface = pygame.Surface((screen_width, screen_height))
    # Creates a new mask where every bit on the screen is on
    full_screen_mask = pygame.mask.from_surface(full_screen_surface)
    # Now turn all of them off (because we're going to impose a different mask)
    # onto this, and we want only those imposed bits to be on
    full_screen_mask.invert()

    pygame.draw.rect(screen, "darkolivegreen4", pygame.Rect(0, 0, screen_width, screen_height))
    start_button = SLButton([20, 20], full_screen_mask.copy(), "Images\endturn.png")
    screen.blit(start_button.pygame_surface, start_button.top_left_corner)
    other_start_button = SLButton([160, 20], full_screen_mask.copy(), "Images\endturn.png")
    screen.blit(other_start_button.pygame_surface, other_start_button.top_left_corner)

    screen_width, screen_height, map_setting_str = menu_screen_loop(start_button, other_start_button, clock, framerate)
    tile_grid, tile_grid_size, faction_turn, num_of_factions, faction_list, opponent, endturn_button, screen = startup(clock, framerate, screen, screen_width, screen_height, map_setting_str)
    highlighted_tile = None

    while True:
        # For now, faction_turn == 0 is the player's turn, faction_turn == 1 is
        # the AI turn
        if (faction_turn != 0):
            opponent.AI_turn()
            faction_turn = game_functions.advance_turn(faction_turn, num_of_factions)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if (faction_turn == 0):
                            if (endturn_button.pygame_mask.get_at(event.pos) == 1):
                                faction_turn = game_functions.advance_turn(faction_turn, num_of_factions)
                            else:
                                for i in range(tile_grid_size):
                                    for j in range(tile_grid_size):
                                        try:
                                            if tile_grid[i][j].pygame_mask.get_at(event.pos) == 1:
                                                if (highlighted_tile == None):
                                                    if (tile_grid[i][j].type != SLTile.Type.BORDER):
                                                        if (tile_grid[i][j].occupant != None):
                                                            if (tile_grid[i][j].occupant.faction == faction_list[faction_turn]):
                                                                highlighted_tile = tile_grid[i][j]
                                                                screen.blit(pygame.image.load(base_game_functions.get_selective_image_str("Images\yellow_hex.png", map_setting_str)), tile_grid[i][j].top_left_corner)
                                                        else:
                                                            highlighted_tile = tile_grid[i][j]
                                                            screen.blit(pygame.image.load(base_game_functions.get_selective_image_str("Images\yellow_hex.png", map_setting_str)), tile_grid[i][j].top_left_corner)
                                                else:
                                                    if (tile_grid[i][j] == highlighted_tile):
                                                        screen.blit(highlighted_tile.pygame_surface, highlighted_tile.top_left_corner)
                                                        if (highlighted_tile.occupant != None):
                                                            screen.blit(highlighted_tile.occupant.pygame_surface, highlighted_tile.top_left_corner)
                                                            game_functions.blit_health(highlighted_tile.occupant, screen, map_setting_str)
                                                        if (highlighted_tile.owner != None):
                                                            game_functions.blit_borders(highlighted_tile, highlighted_tile.owner.color, screen)
                                                        highlighted_tile = None
                                                    elif (highlighted_tile.occupant != None):
                                                    # checks if there is an occupant on the highlighted tile
                                                        neighbors = game_functions.find_neighbors(highlighted_tile, tile_grid)
                                                        for tile in neighbors:
                                                            if (tile_grid[i][j] == tile):
                                                            # checks if the clicked tile is in the surrounding tiles of the highlighted tile
                                                                if (tile.occupant != None):
                                                                # checks if there is an occupant on the selected tile
                                                                    if (tile.occupant.faction == highlighted_tile.occupant.faction):
                                                                    # if the selected tile's occupant is of the same faction as the player, it will swap the two occupants
                                                                        movement.swap_occupants(highlighted_tile, tile, screen)
                                                                        game_functions.blit_borders(tile, tile.owner.color, screen)
                                                                        game_functions.blit_borders(highlighted_tile, tile.owner.color, screen)
                                                                        highlighted_tile = None
                                                                    else:
                                                                    # if the selected tile's occupant is of a different faction, a battle will ensue
                                                                        attacker = highlighted_tile.occupant
                                                                        defender = tile.occupant
                                                                        result = combat.battle(attacker, defender, tile_grid, screen)
                                                                        if (result == 1):
                                                                        # defender died
                                                                            game_functions.remove_entity(defender)
                                                                        elif (result == 2):
                                                                        # attacker died
                                                                            game_functions.remove_entity(attacker)
                                                                        elif (result == 3):
                                                                        # both died
                                                                            game_functions.remove_entity(attacker)
                                                                            game_functions.remove_entity(defender)
                                                                else:
                                                                # if there is no occupant on the selected tile, the highlighted tile's occupant will move to the selected tile
                                                                    movement.move_occupant(highlighted_tile, tile, screen, tile_grid)
                                                                    for claimed in (game_functions.find_empty_neighbors(tile, tile_grid) + [tile]):
                                                                        if (claimed.owner == faction_list[faction_turn]):
                                                                            game_functions.blit_borders(claimed, claimed.owner.color, screen)
                                                                    highlighted_tile = None
                                                                break
                                            else:
                                                pass
                                        except IndexError:
                                            pass
                                else:
                                    pass
        pygame.display.update()
        clock.tick(framerate)

if __name__ == "__main__":
    main()
