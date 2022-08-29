import pygame
import game_functions
from SLTile import SLTile
from SLBrigade import SLBrigade
from SLBuilding import SLBuilding
from SLFaction import SLFaction

class SLRegion:
    # A region is an area of tiles owned by a faction which are all connected
    # Variables: tiles - the tiles which encompass the region
    #            contains_capital - a bool indicating whether the region contains the faction's capital

    def __init__(self, tiles):
        # Initializes the Region
        # Parameters: self - the Region object
        #             tiles - the tiles contained in the region

        self.tiles = tiles
        self.contains_capital = False


def BFS(origin: SLTile, visited, map):
    # Runs Breadth First Search from the origin tile to find connected tiles of the same faction
    # Will only continue searching if found tiles are of same faction as origin
    # Parameters: origin - SLTile, the origin of the BFS
    #             visited - the grid keeping track of visited tiles
    #             map - the grid which contains the tiles of the game
    # Returns a list of the tiles that were found and of the same faction as origin

    # the tiles which are found and have to be returned
    tiles = []

    # the queue containing the tiles which need to be searched
    queue = []
    queue.append(origin)

    y, x = origin.location
    visited[y][x] = True
    faction = origin.owner

    while queue:
        current = queue.pop(0)
        tiles.append(current)

        for tile in game_functions.find_neighbors(current, map):
            y, x = tile.location
            if (not visited[y][x]):
                visited[y][x] = True
                if (tile.owner == faction):
                    queue.append(tile)
    
    return tiles


def turn_crunch(faction: SLFaction, map, map_size):
    # Enacts the turn crunch:
    #   - Applies any resource generation in the faction
    #   - Applies attrition to affected units owned by the faction
    # Parameters: faction - SLFaction, the faction whose turn is being crunched
    #             map - the grid which contains the tiles of the game
    #             map_size - the size of the map

    # visited 2D array keeps track of whether tile was visited or not
    visited = [[False] * map_size] * map_size 

    # regions array keeps track of regions owned by the faction
    # a region being defined as an area of tiles owned by a faction which are all connected
    regions = []

    for i in range(map_size):
        for j in range(map_size):
            if (not visited[i][j]):
                if (map[i][j].owner == faction):
                    region = SLRegion(BFS(map[i][j], visited))
                    regions.append(region)
                else:
                    visited[i][j] = True
    
