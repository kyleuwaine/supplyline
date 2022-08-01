import pygame
from sys import exit
from SLTile import SLTile
from SLBrigade import SLBrigade
from startup import startup

pygame.init()
clock, framerate, screen, tile_grid, tile_grid_size = startup()
selected_tile = None
x = 0
y = 0
faction_turn = 0
num_of_players = 2
tile_grid[1][1].occupant = SLBrigade("Tank", None)
screen.blit(tile_grid[1][1].occupant.pygame_surface, tile_grid[1][1].top_left_corner)

def advance_turn():
    faction_turn += 1
    faction_turn = faction_turn % num_of_players


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i in range(tile_grid_size):
                    for j in range(tile_grid_size):
                        try:
                            if tile_grid[i][j].pygame_mask.get_at(event.pos) == 1:
                                if (selected_tile == None):
                                    if (tile_grid[i][j].type != SLTile.Type.BORDER):
                                        selected_tile = tile_grid[i][j]
                                        screen.blit(pygame.image.load("Images\yellow_hex.png"), tile_grid[i][j].top_left_corner)
                                        x = j
                                        y = i
                                else:
                                    if (tile_grid[i][j] == selected_tile):
                                        screen.blit(tile_grid[i][j].pygame_surface, tile_grid[i][j].top_left_corner)
                                        if (tile_grid[i][j].occupant != None):
                                            screen.blit(tile_grid[i][j].occupant.pygame_surface, tile_grid[i][j].top_left_corner)
                                        selected_tile = None
                                    elif (y % 2 == 0):
                                        if (True):
                                            if (i == y and j == x + 1):
                                                screen.blit(tile_grid[y][x].pygame_surface, tile_grid[y][x].top_left_corner)
                                                tile_grid[i][j].occupant = tile_grid[y][x].occupant
                                                tile_grid[y][x].occupant = None
                                                screen.blit(tile_grid[i][j].occupant.pygame_surface, tile_grid[i][j].top_left_corner)
                                                selected_tile = None
                                            elif (i == y and j == x - 1):
                                                screen.blit(tile_grid[y][x].pygame_surface, tile_grid[y][x].top_left_corner)
                                                tile_grid[i][j].occupant = tile_grid[y][x].occupant
                                                tile_grid[y][x].occupant = None
                                                screen.blit(tile_grid[i][j].occupant.pygame_surface, tile_grid[i][j].top_left_corner)
                                                selected_tile = None
                                            elif (i == y - 1 and j == x):
                                                screen.blit(tile_grid[y][x].pygame_surface, tile_grid[y][x].top_left_corner)
                                                tile_grid[i][j].occupant = tile_grid[y][x].occupant
                                                tile_grid[y][x].occupant = None
                                                screen.blit(tile_grid[i][j].occupant.pygame_surface, tile_grid[i][j].top_left_corner)
                                                selected_tile = None
                                            elif (i == y - 1 and j == x + 1):
                                                screen.blit(tile_grid[y][x].pygame_surface, tile_grid[y][x].top_left_corner)
                                                tile_grid[i][j].occupant = tile_grid[y][x].occupant
                                                tile_grid[y][x].occupant = None
                                                screen.blit(tile_grid[i][j].occupant.pygame_surface, tile_grid[i][j].top_left_corner)
                                                selected_tile = None
                                            elif (i == y + 1 and j == x):
                                                screen.blit(tile_grid[y][x].pygame_surface, tile_grid[y][x].top_left_corner)
                                                tile_grid[i][j].occupant = tile_grid[y][x].occupant
                                                tile_grid[y][x].occupant = None
                                                screen.blit(tile_grid[i][j].occupant.pygame_surface, tile_grid[i][j].top_left_corner)
                                                selected_tile = None
                                            elif (i == y + 1 and j == x + 1):
                                                screen.blit(tile_grid[y][x].pygame_surface, tile_grid[y][x].top_left_corner)
                                                tile_grid[i][j].occupant = tile_grid[y][x].occupant
                                                tile_grid[y][x].occupant = None
                                                screen.blit(tile_grid[i][j].occupant.pygame_surface, tile_grid[i][j].top_left_corner)
                                                selected_tile = None
                                    else:
                                        if (i == y and j == x + 1):
                                            screen.blit(tile_grid[y][x].pygame_surface, tile_grid[y][x].top_left_corner)
                                            tile_grid[i][j].occupant = tile_grid[y][x].occupant
                                            tile_grid[y][x].occupant = None
                                            screen.blit(tile_grid[i][j].occupant.pygame_surface, tile_grid[i][j].top_left_corner)
                                            selected_tile = None
                                        elif (i == y and j == x - 1):
                                            screen.blit(tile_grid[y][x].pygame_surface, tile_grid[y][x].top_left_corner)
                                            tile_grid[i][j].occupant = tile_grid[y][x].occupant
                                            tile_grid[y][x].occupant = None
                                            screen.blit(tile_grid[i][j].occupant.pygame_surface, tile_grid[i][j].top_left_corner)
                                            selected_tile = None
                                        elif (i == y - 1 and j == x):
                                            screen.blit(tile_grid[y][x].pygame_surface, tile_grid[y][x].top_left_corner)
                                            tile_grid[i][j].occupant = tile_grid[y][x].occupant
                                            tile_grid[y][x].occupant = None
                                            screen.blit(tile_grid[i][j].occupant.pygame_surface, tile_grid[i][j].top_left_corner)
                                            selected_tile = None
                                        elif (i == y - 1 and j == x - 1):
                                            screen.blit(tile_grid[y][x].pygame_surface, tile_grid[y][x].top_left_corner)
                                            tile_grid[i][j].occupant = tile_grid[y][x].occupant
                                            tile_grid[y][x].occupant = None
                                            screen.blit(tile_grid[i][j].occupant.pygame_surface, tile_grid[i][j].top_left_corner)
                                            selected_tile = None
                                        elif (i == y + 1 and j == x):
                                            screen.blit(tile_grid[y][x].pygame_surface, tile_grid[y][x].top_left_corner)
                                            tile_grid[i][j].occupant = tile_grid[y][x].occupant
                                            tile_grid[y][x].occupant = None
                                            screen.blit(tile_grid[i][j].occupant.pygame_surface, tile_grid[i][j].top_left_corner)
                                            selected_tile = None
                                        elif (i == y + 1 and j == x - 1):
                                            screen.blit(tile_grid[y][x].pygame_surface, tile_grid[y][x].top_left_corner)
                                            tile_grid[i][j].occupant = tile_grid[y][x].occupant
                                            tile_grid[y][x].occupant = None
                                            screen.blit(tile_grid[i][j].occupant.pygame_surface, tile_grid[i][j].top_left_corner)
                                            selected_tile = None
                            else:
                                pass
                        except IndexError:
                            pass


    #screen.blit(test_surface, (200, 100))

    pygame.display.update()
    clock.tick(framerate)
