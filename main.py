import pygame
from sys import exit
from SLTile import SLTile
from SLBrigade import SLBrigade
from startup import startup
from SLButton import SLButton
from SLBuilding import SLBuilding
from turn_crunch import turn_crunch
import game_functions
import base_game_functions
import combat
import movement
import json

"""
This file contains the main function for the Supplyline program, as well as other
functions that are needed to handle the main event loop. main() first
creates a launcher that contains options for game settings, then calls
menu_screen_loop(), which acts as the event loop until the game is started by
indicating an appropriate option. After the game is started, main() acts as the
event loop for the Supplyline program.

Author: Kyle Uwaine and Victor Nault
Date: 9/11/2022
"""


def menu_screen_loop(small_screen_button: SLButton, big_screen_button: SLButton, viet_button: SLButton, clock, framerate: int):
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
                        viet_button.pygame_mask.clear()
                        return 1366, 768, "big_tiles_debug_map"
                        #start_game = True
                    if (big_screen_button.pygame_mask.get_at(event.pos) == 1):
                        small_screen_button.pygame_mask.clear()
                        big_screen_button.pygame_mask.clear()
                        viet_button.pygame_mask.clear()
                        return 1920, 1080, "small_tiles_std_map"
                    if (viet_button.pygame_mask.get_at(event.pos) == 1):
                        small_screen_button.pygame_mask.clear()
                        big_screen_button.pygame_mask.clear()
                        viet_button.pygame_mask.clear()
                        with open("custom_map.json", "r") as input:
                            input_lst = json.load(input)
                        tokens = str(input_lst).split(". ")
                        #print(tokens[4])
                        if (tokens[4] == "big_tiles_debug_map"):
                            return 1366, 768, "custom_big_tiles_debug_map"
                        if (tokens[4] == "small_tiles_std_map"):
                            return 1920, 1080, "custom_small_tiles_std_map"
                        if (tokens[4] == "big_tiles_std_map"):
                            return 1366, 768, "custom_big_tiles_std_map"

        pygame.display.update()
        clock.tick(1)

def player_defeat(screen_width, screen_height, clock, screen):
    pygame.draw.rect(screen, "white", pygame.Rect(0, 0, screen_width, screen_height))
    font = pygame.font.SysFont("arial", 100)
    defeat_surface = font.render("Lose...", None, pygame.Color("black"))
    screen.blit(defeat_surface, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.display.update()
        clock.tick(10)

def player_victory(screen_width, screen_height, clock, screen):
    pygame.draw.rect(screen, "white", pygame.Rect(0, 0, screen_width, screen_height))
    font = pygame.font.SysFont("arial", 100)
    victory_surface = font.render("Win!", None, pygame.Color("black"))
    screen.blit(victory_surface, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.display.update()
        clock.tick(10)

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
    start_button = SLButton([20, 20], full_screen_mask.copy(), "Images/_endturn.png")
    screen.blit(start_button.pygame_surface, start_button.top_left_corner)
    other_start_button = SLButton([160, 20], full_screen_mask.copy(), "Images/_endturn.png")
    screen.blit(other_start_button.pygame_surface, other_start_button.top_left_corner)
    viet_start_button = SLButton([300, 20], full_screen_mask.copy(), "Images/_custommap.png")
    screen.blit(viet_start_button.pygame_surface,viet_start_button.top_left_corner)

    screen_width, screen_height, map_setting_str = menu_screen_loop(start_button, other_start_button, viet_start_button, clock, framerate)
    # Set below to true to enable the export map button
    export_map_bool = False
    tile_grid, tile_grid_size, faction_turn, num_of_factions, faction_list, opponent, endturn_button, buildbarracks_button, buildfort_button, buildtank_button, buildinfantry_button, exportmap_button, map_setting_str, screen = startup(clock, framerate, screen, screen_width, screen_height, map_setting_str, export_map_bool)
    highlighted_tile = None
    recruiting = None
    build_loc_tiles = []
    valid_moves = []

    while True:
        # For now, faction_turn == 0 is the player's turn, faction_turn == 1 is
        # the AI turn
        if (faction_turn != 0):
            opponent.AI_turn()
            faction_turn = base_game_functions.advance_turn(faction_turn, num_of_factions)
        if (faction_list[0].is_defeated == True):
            player_defeat(screen_width, screen_height, clock, screen)
        # Change this if more than two factions are ever implemented
        if (faction_list[1].is_defeated == True):
            player_victory(screen_width, screen_height, clock, screen)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if (faction_turn == 0):
                            game_functions.blit_resource_counts(faction_list[faction_turn], screen)

                            if (export_map_bool == True):
                                if (exportmap_button.pygame_mask.get_at(event.pos) == 1):
                                    game_functions.export_map(tile_grid, tile_grid_size)

                            # Check if endturn button gets pressed by player
                            if (endturn_button.pygame_mask.get_at(event.pos) == 1):
                                turn_crunch(faction_list[faction_turn], tile_grid, tile_grid_size, screen)
                                faction_turn = base_game_functions.advance_turn(faction_turn, num_of_factions)

                            # Check if build barracks button gets pressed by player
                            if ((buildbarracks_button.pygame_mask.get_at(event.pos) == 1) and (buildbarracks_button.active == True)):
                                highlighted_tile.occupant = SLBuilding(SLBuilding.Type.BARRACKS, faction_list[0], highlighted_tile, faction_list[0].building_id_counter)
                                faction_list[0].building_dict.update({faction_list[0].building_id_counter: highlighted_tile.occupant})
                                faction_list[0].building_id_counter += 1
                                game_functions.reblit_tile(highlighted_tile, screen)
                                highlighted_tile = None
                                buildbarracks_button.active = False
                                screen.blit(buildbarracks_button.pygame_surface, buildbarracks_button.top_left_corner)
                                # Also deactivate the fort build button in case the player tries to build a fort right after building a barracks
                                buildfort_button.active = False
                                screen.blit(buildfort_button.pygame_surface, buildfort_button.top_left_corner)
                                faction_list[faction_turn].metals -= 5
                                game_functions.blit_resource_counts(faction_list[faction_turn], screen)

                            # Check if build fort button gets pressed by player
                            if ((buildfort_button.pygame_mask.get_at(event.pos) == 1) and (buildfort_button.active == True)):
                                highlighted_tile.occupant = SLBuilding(SLBuilding.Type.FORT, faction_list[0], highlighted_tile, faction_list[0].building_id_counter)
                                faction_list[0].building_dict.update({faction_list[0].building_id_counter: highlighted_tile.occupant})
                                faction_list[0].building_id_counter += 1
                                game_functions.reblit_tile(highlighted_tile, screen)
                                highlighted_tile = None
                                buildfort_button.active = False
                                screen.blit(buildfort_button.pygame_surface, buildfort_button.top_left_corner)
                                # Also deactivate the barracks build button in case the player tries to build a barracks right after building a fort
                                buildbarracks_button.active = False
                                screen.blit(buildbarracks_button.pygame_surface, buildbarracks_button.top_left_corner)
                                faction_list[faction_turn].metals -= 5
                                game_functions.blit_resource_counts(faction_list[faction_turn], screen)

                            # Check if build tank button gets pressed by player
                            if ((buildtank_button.pygame_mask.get_at(event.pos) == 1) and (buildtank_button.active == True)):
                                valid_rec_locs = game_functions.find_valid_rec_locs(highlighted_tile, tile_grid)
                                if (valid_rec_locs != []):
                                    # Note: recuiting is set in here so that if there are no valid locations the player isn't stuck, since recuiting being set disables some things
                                    # It would be helpful in the future to have a "cancel recuiting" button to avoid this and related situations
                                    recruiting = "Tank"
                                    build_loc_tiles = valid_rec_locs
                                    for tile in build_loc_tiles:
                                        screen.blit(pygame.image.load(base_game_functions.get_selective_image_str("Images/_purple_hex.png", map_setting_str)), tile.top_left_corner)
                                    buildtank_button.active = False
                                    screen.blit(buildtank_button.pygame_surface, buildtank_button.top_left_corner)
                                    # So the player can't build a tank then immediately build infantry, which will break because the barracks will be deactivated during this
                                    buildinfantry_button.active = False
                                    screen.blit(buildinfantry_button.pygame_surface, buildinfantry_button.top_left_corner)

                                    game_functions.reblit_tile(highlighted_tile, screen)
                                    highlighted_tile = None

                            # Check if build infantry button gets pressed by player
                            if ((buildinfantry_button.pygame_mask.get_at(event.pos) == 1) and (buildinfantry_button.active == True)):
                                valid_rec_locs = game_functions.find_valid_rec_locs(highlighted_tile, tile_grid)
                                if (valid_rec_locs != []):
                                    recruiting = "Infantry"
                                    build_loc_tiles = valid_rec_locs
                                    for tile in build_loc_tiles:
                                        screen.blit(pygame.image.load(base_game_functions.get_selective_image_str("Images/_purple_hex.png", map_setting_str)), tile.top_left_corner)
                                    buildinfantry_button.active = False
                                    screen.blit(buildinfantry_button.pygame_surface, buildinfantry_button.top_left_corner)
                                    # So the player can't build infantry then immediately build a tank, which will break because the barracks will be deactivated during this
                                    buildtank_button.active = False
                                    screen.blit(buildtank_button.pygame_surface, buildtank_button.top_left_corner)

                                    game_functions.reblit_tile(highlighted_tile, screen)
                                    highlighted_tile = None


                            # If no UI buttons are pressed then check which tile on the map got pressed
                            else:
                                for i in range(tile_grid_size):
                                    for j in range(tile_grid_size):
                                        try:
                                            if tile_grid[i][j].pygame_mask.get_at(event.pos) == 1:

                                                # If no tiles are highlighted, player could be selecting tile to highlight or a selecting a tile to build a unit on
                                                if (highlighted_tile == None):

                                                    # If recruiting is empty, then the player is selecting a tile to highlight
                                                    if (recruiting == None):

                                                        # If either build unit buttons are active, this means the player selected a tile containing a barracks previously but didn't press the build button.
                                                        # In this case, the buttons are deactivated
                                                        if (buildtank_button.active == True):
                                                            buildtank_button.active = False
                                                            screen.blit(buildbarracks_button.pygame_surface, buildbarracks_button.top_left_corner)
                                                            for tile in build_loc_tiles:
                                                                    screen.blit(tile.pygame_surface, tile.top_left_corner)
                                                                    game_functions.blit_borders(tile, tile.owner.color, screen)

                                                        if (buildinfantry_button.active == True):
                                                            buildinfantry_button.active = False
                                                            screen.blit(buildbarracks_button.pygame_surface, buildbarracks_button.top_left_corner)
                                                            for tile in build_loc_tiles:
                                                                    screen.blit(tile.pygame_surface, tile.top_left_corner)
                                                                    game_functions.blit_borders(tile, tile.owner.color, screen)


                                                        # Check if the tile pressed is within the map borders
                                                        if (tile_grid[i][j].type != SLTile.Type.BORDER):

                                                            # Check if the tile pressed has an occupant
                                                            if (tile_grid[i][j].occupant != None):

                                                                # Check if the occupant is of the same faction as player
                                                                if (tile_grid[i][j].occupant.faction == faction_list[faction_turn]):

                                                                    # If the occupant is a brigade, then the tile is highlighted and the possible moves for the brigade are shown
                                                                    if (tile_grid[i][j].occupant.is_building == False):
                                                                        highlighted_tile = tile_grid[i][j]
                                                                        screen.blit(pygame.image.load(base_game_functions.get_selective_image_str("Images/_yellow_hex.png", map_setting_str)), tile_grid[i][j].top_left_corner)
                                                                        valid_moves = movement.find_valid_moves(highlighted_tile, True, tile_grid, screen)

                                                                    # If not then the occupant is a building
                                                                    elif (tile_grid[i][j].occupant.is_building == True):

                                                                        # If the building is the Capital or a barracks, then the player may be trying to recruit a brigade
                                                                        if (tile_grid[i][j].occupant.type == SLBuilding.Type.CAPITAL or tile_grid[i][j].occupant.type == SLBuilding.Type.BARRACKS):

                                                                            # Check the capability of the faction to recruit brigades (based on force limit and available resources)
                                                                            below_cap, can_build_infantry, can_build_tank = faction_list[faction_turn].rec_capability()
                                                                            if (below_cap and (can_build_infantry or can_build_tank)):
                                                                                highlighted_tile = tile_grid[i][j]
                                                                                screen.blit(pygame.image.load(base_game_functions.get_selective_image_str("Images/_yellow_hex.png", map_setting_str)), highlighted_tile.top_left_corner)
                                                                                if (can_build_infantry):
                                                                                    buildinfantry_button.active = True
                                                                                    screen.blit(buildinfantry_button.alt_pygame_surface, buildinfantry_button.top_left_corner)
                                                                                if (can_build_tank):
                                                                                    buildtank_button.active = True
                                                                                    screen.blit(buildtank_button.alt_pygame_surface, buildtank_button.top_left_corner)

                                                                        # If it's another type of building then just highlight the tile
                                                                        else:
                                                                            highlighted_tile = tile_grid[i][j]
                                                                            screen.blit(pygame.image.load(base_game_functions.get_selective_image_str("Images/_yellow_hex.png", map_setting_str)), tile_grid[i][j].top_left_corner)

                                                            # If there is no occupant, then just highlight the tile
                                                            else:
                                                                highlighted_tile = tile_grid[i][j]
                                                                screen.blit(pygame.image.load(base_game_functions.get_selective_image_str("Images/_yellow_hex.png", map_setting_str)), tile_grid[i][j].top_left_corner)

                                                                # If they highlight a tile owned by them, player may be trying to build a building, so activate the build buildings buttons
                                                                if (highlighted_tile.owner == faction_list[faction_turn]):
                                                                    # But only if they have the metals...
                                                                    if (faction_list[faction_turn].metals >= 5):
                                                                        buildbarracks_button.active = True
                                                                        screen.blit(buildbarracks_button.alt_pygame_surface, buildbarracks_button.top_left_corner)
                                                                        buildfort_button.active = True
                                                                        screen.blit(buildfort_button.alt_pygame_surface, buildfort_button.top_left_corner)

                                                    # If recruiting is not empty, then player is selecting a tile to build a unit on
                                                    else:

                                                        # Check if the tile being selected is valid to build on
                                                        if (tile_grid[i][j] in build_loc_tiles):
                                                            #build_loc_tiles.remove(tile_grid[i][j])
                                                            for tile in build_loc_tiles:
                                                                screen.blit(tile.pygame_surface, tile.top_left_corner)
                                                                game_functions.blit_borders(tile, tile.owner.color, screen)
                                                            build_loc_tiles = []

                                                            # If recruting contains "Tank", then build a tank brigade on selected tile
                                                            if (recruiting == "Tank"):
                                                                tile_grid[i][j].occupant = SLBrigade("Tank", faction_list[0], tile_grid[i][j], faction_list[0].brigade_id_counter)
                                                                faction_list[0].brigade_dict.update({faction_list[0].brigade_id_counter: tile_grid[i][j].occupant})
                                                                faction_list[0].brigade_id_counter += 1
                                                                game_functions.reblit_tile(tile_grid[i][j], screen)
                                                                faction_list[faction_turn].metals -= 5
                                                                game_functions.blit_resource_counts(faction_list[faction_turn], screen)

                                                            # If recruting contains "Infantry", then build an infantry brigade on selected tile
                                                            elif (recruiting == "Infantry"):
                                                                tile_grid[i][j].occupant = SLBrigade("Infantry", faction_list[0], tile_grid[i][j], faction_list[0].brigade_id_counter)
                                                                faction_list[0].brigade_dict.update({faction_list[0].brigade_id_counter: tile_grid[i][j].occupant})
                                                                faction_list[0].brigade_id_counter += 1
                                                                game_functions.reblit_tile(tile_grid[i][j], screen)
                                                                faction_list[faction_turn].metals -= 5
                                                                game_functions.blit_resource_counts(faction_list[faction_turn], screen)
                                                                pass

                                                            recruiting = None

                                                # A tile is already highlighted
                                                else:

                                                    # If the tile selected is the highlighted tile, unhighlight it
                                                    if (tile_grid[i][j] == highlighted_tile):

                                                        # If the build barracks button is active, deactivate it
                                                        if (buildbarracks_button.active == True):
                                                            # Should be deactivate button function
                                                            buildbarracks_button.active = False
                                                            screen.blit(buildbarracks_button.pygame_surface, buildbarracks_button.top_left_corner)

                                                        # If the build fort button is active, deactivate it
                                                        if (buildfort_button.active == True):
                                                            # Should be deactivate button function
                                                            buildfort_button.active = False
                                                            screen.blit(buildfort_button.pygame_surface, buildfort_button.top_left_corner)

                                                        # If the build tank button is active, deactivate it
                                                        if (buildtank_button.active == True):
                                                            buildtank_button.active = False
                                                            screen.blit(buildtank_button.pygame_surface, buildtank_button.top_left_corner)

                                                        # If the build infantry button is active, deactivate it
                                                        if (buildinfantry_button.active == True):
                                                            buildinfantry_button.active = False
                                                            screen.blit(buildinfantry_button.pygame_surface, buildinfantry_button.top_left_corner)

                                                        # Unhighlight any highlighted tiles
                                                        game_functions.reblit_tile(highlighted_tile, screen)
                                                        for tile in valid_moves:
                                                            game_functions.reblit_tile(tile, screen)
                                                        valid_moves = []
                                                        highlighted_tile = None

                                                    # Check if there is an occupant on the highlighted tile
                                                    elif (highlighted_tile.occupant != None):

                                                        # Attempt to move the occupant on the highlighted tile to the tile that was clicked
                                                        moved, eliminated = movement.attempt_move(highlighted_tile, tile_grid[i][j], valid_moves, tile_grid, screen)

                                                        # Check if move was successful
                                                        if (moved):
                                                            highlighted_tile = None
                                                            valid_moves = []
                                                            for entity in eliminated:
                                                                game_functions.remove_entity(entity)
                                                            eliminated = []
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
