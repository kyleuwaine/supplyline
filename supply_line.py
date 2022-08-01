import pygame
from sys import exit
from SLTile import SLTile
from SLBrigade import SLBrigade
from startup import startup
import game_functions

pygame.init()
clock, framerate, screen, tile_grid, tile_grid_size, faction_turn, num_of_factions = startup()
highlighted_tile = None
x = 0
y = 0

while True:
    if (faction_turn != 0):
        pass
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if (faction_turn == 0):
                    for i in range(tile_grid_size):
                        for j in range(tile_grid_size):
                            try:
                                if tile_grid[i][j].pygame_mask.get_at(event.pos) == 1:
                                    if (highlighted_tile == None):
                                        if (tile_grid[i][j].type != SLTile.Type.BORDER):
                                            highlighted_tile = tile_grid[i][j]
                                            screen.blit(pygame.image.load("Images\yellow_hex.png"), tile_grid[i][j].top_left_corner)
                                            x = j
                                            y = i
                                    else:
                                        if (tile_grid[i][j] == highlighted_tile):
                                            screen.blit(tile_grid[i][j].pygame_surface, tile_grid[i][j].top_left_corner)
                                            if (tile_grid[i][j].occupant != None):
                                                screen.blit(tile_grid[i][j].occupant.pygame_surface, tile_grid[i][j].top_left_corner)
                                            highlighted_tile = None
                                        else:
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
