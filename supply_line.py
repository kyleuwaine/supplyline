import pygame
from sys import exit
from SLTile import SLTile
from SLBrigade import SLBrigade
from startup import startup
from SLButton import SLButton
import game_functions
import combat
import movement

pygame.init()
screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Supply Line")
clock = pygame.time.Clock()
framerate = 10
full_screen_surface = pygame.Surface((screen_width, screen_height))
full_screen_mask = pygame.mask.from_surface(full_screen_surface)
full_screen_mask.invert()

pygame.draw.rect(screen, "darkolivegreen4", pygame.Rect(0, 0, screen_width, screen_height))
start_button = SLButton([20, 20], full_screen_mask, "Images\endturn.png")
screen.blit(start_button.pygame_surface, start_button.top_left_corner)


while True:
    start_game = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if (start_button.pygame_mask.get_at(event.pos) == 1):
                    start_button.pygame_mask.clear()
                    start_game = True

    pygame.display.update()
    clock.tick(framerate)
    if(start_game == True):
        break

pygame.draw.rect(screen, "black", pygame.Rect(0, 0, screen_width, screen_height))

tile_grid, tile_grid_size, faction_turn, num_of_factions, faction_list, opponent, endturn_button = startup(clock, framerate, screen)
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
                                                                    movement.swap_occupants(highlighted_tile, tile, screen)
                                                                    highlighted_tile = None
                                                                else:
                                                                    combat.battle(highlighted_tile.occupant, tile.occupant, screen)
                                                            else:
                                                                movement.move_occupant(highlighted_tile, tile, screen)
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
