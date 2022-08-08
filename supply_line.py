import pygame
from sys import exit
from SLTile import SLTile
from SLBrigade import SLBrigade
from startup import startup
import game_functions

pygame.init()
clock, framerate, screen, tile_grid, tile_grid_size, faction_turn, num_of_factions, faction_list, opponent, endturn_mask = startup()
highlighted_tile = None
x = 0
y = 0

while True:
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
                        if (endturn_mask.get_at(event.pos) == 1):
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
                                                            screen.blit(pygame.image.load("Images\yellow_hex.png"), tile_grid[i][j].top_left_corner)
                                                            x = j
                                                            y = i
                                                    else:
                                                        highlighted_tile = tile_grid[i][j]
                                                        screen.blit(pygame.image.load("Images\yellow_hex.png"), tile_grid[i][j].top_left_corner)
                                                        x = j
                                                        y = i
                                            else:
                                                if (tile_grid[i][j] == highlighted_tile):
                                                    screen.blit(highlighted_tile.pygame_surface, highlighted_tile.top_left_corner)
                                                    if (highlighted_tile.occupant != None):
                                                        screen.blit(highlighted_tile.occupant.pygame_surface, highlighted_tile.top_left_corner)
                                                    highlighted_tile = None
                                                elif (highlighted_tile.occupant != None):
                                                    neighbors = game_functions.find_neighbors(highlighted_tile, tile_grid)
                                                    for tile in neighbors:
                                                        if (tile_grid[i][j] == tile):
                                                            if (tile.occupant != None):
                                                                if (tile.occupant.faction == highlighted_tile.occupant.faction):
                                                                    game_functions.swap_occupants(highlighted_tile, tile, screen)
                                                                    faction_turn = game_functions.advance_turn(faction_turn, num_of_factions)
                                                                    highlighted_tile = None
                                                                else:
                                                                    pass # Battle
                                                            else:
                                                                game_functions.move_occupant(highlighted_tile, tile, screen)
                                                                faction_turn = game_functions.advance_turn(faction_turn, num_of_factions)
                                                                highlighted_tile = None
                                                            break
                                        else:
                                            pass
                                    except IndexError:
                                        pass
                            else:
                                pass


    #screen.blit(test_surface, (200, 100))

    pygame.display.update()
    clock.tick(framerate)
