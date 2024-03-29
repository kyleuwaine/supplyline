from threading import currentThread
import pygame
import game_functions
import movement
from SLTile import SLTile
from SLBrigade import SLBrigade
from SLBuilding import SLBuilding
from SLFaction import SLFaction

class SLRegion:
    # A region is an area of tiles owned by a faction which are all connected
    # Variables: tiles - the tiles which encompass the region
    #            faction - the faction which owns the region
    #            contains_capital - a bool indicating whether the region contains the faction's capital

    def __init__(self, faction, tiles, contains_capital):
        # Initializes the Region
        # Parameters: self - the Region object
        #             faction - SLFaction, the faction which owns the region
        #             tiles - the tiles contained in the region

        self.faction = faction
        self.tiles = tiles
        self.contains_capital = contains_capital


def BFS(origin: SLTile, visited, map):
    # Runs Breadth First Search from the origin tile to find connected tiles of the same faction
    # Will only continue searching if found tiles are of same faction as origin
    # Parameters: origin - SLTile, the origin of the BFS
    #             visited - the grid keeping track of visited tiles
    #             map - the grid which contains the tiles of the game
    # Returns a list of the tiles that were found and of the same faction as origin

    has_capital = False

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
        if (current.occupant):
            if (current.occupant.is_building):
                if (current.occupant.type == SLBuilding.Type.CAPITAL):
                    has_capital = True

        for tile in game_functions.find_neighbors(current, map):
            y, x = tile.location
            if (not visited[y][x]):
                visited[y][x] = True
                if (tile.owner == faction):
                    queue.append(tile)

    return tiles, has_capital


def calculate_attrition(supply, demand):
    # Calculates the attrition applied based on the supply and demand
    # Parameters: supply - the amount of specific resource available
    #             demand - the amount of specific resource required
    # Returns the amount of attrition needed to be applied

    if (supply == 0):
        return 20

    if (demand // supply == 1):
        return 5
    elif (demand // supply == 2):
        return 10
    elif (demand // supply == 3):
        return 15
    elif (demand // supply == 4):
        return 20
    else:
        return 20


def apply_generation_and_attrition(region: SLRegion, screen):
    # Calculates and applies the resources generated in the region
    # as well as the attrition suffered by brigades within it
    # Parameters: region: SLRegion, the region being analyzed
    #             screen: the screen of the game

    faction = region.faction
    contains_capital_bool = region.contains_capital
    
    infantry = []
    tanks = []

    available_food = 0
    available_fuel = 0
    available_metal = 0
    food_consumption = 0
    fuel_consumption = 0

    for tile in region.tiles:
        if (tile.occupant):
            if (tile.occupant.is_building):
                if (tile.occupant.resource == SLBuilding.Resource.FOOD):
                    available_food += tile.occupant.production
                elif (tile.occupant.resource == SLBuilding.Resource.FUEL):
                    available_fuel += tile.occupant.production
                elif (tile.occupant.resource == SLBuilding.Resource.METALS):
                    available_metal += tile.occupant.production
                elif (tile.occupant.resource == SLBuilding.Resource.NONE):
                    # Attrition damage for disconnected non-resource buildings
                    if (not contains_capital_bool):
                        tile.occupant.health -= 10
                        if (tile.occupant.health <= 0):
                            game_functions.remove_entity(tile.occupant)
                            tile.occupant = None
                        game_functions.reblit_tile(tile, screen)
            else:
                food_consumption += tile.occupant.food_consumption
                fuel_consumption += tile.occupant.fuel_consumption

                if (tile.occupant.type == SLBrigade.BrigadeType.INFANTRY):
                    infantry.append(tile.occupant)
                elif (tile.occupant.type == SLBrigade.BrigadeType.TANK):
                    tanks.append(tile.occupant)

    if (contains_capital_bool):
        available_food += faction.food
        available_fuel += faction.fuel
        available_metal += faction.metals

    if (available_food < food_consumption):
        attrition = calculate_attrition(available_food, food_consumption)
        available_food = 0
        for brigade in infantry:
            brigade.health -= attrition

            if (brigade.health <= 0):
                brigade.location.occupant = None
                game_functions.remove_entity(brigade)

            game_functions.reblit_tile(brigade.location, screen)
    else:
        available_food -= food_consumption

    if (available_fuel < fuel_consumption):
        attrition = calculate_attrition(available_fuel, fuel_consumption)
        available_fuel = 0
        for brigade in tanks:
            brigade.health -= attrition

            if (brigade.health <= 0):
                brigade.location.occupant = None
                game_functions.remove_entity(brigade)

            game_functions.reblit_tile(brigade.location, screen)
    else:
        available_fuel -= fuel_consumption

    if (contains_capital_bool):
        faction.food = available_food
        faction.fuel = available_fuel
        faction.metals = available_metal


def turn_crunch(faction: SLFaction, map, map_size, screen):
    # Enacts the turn crunch:
    #   - Applies any resource generation in the faction
    #   - Applies attrition to affected units owned by the faction
    #   - Applies regeneration to production buildings
    #   - Resets the available moves of brigades owned by the faction back to max
    #   - Checks if the faction has no capital(s). If so, sets defeat flag
    # Parameters: faction - SLFaction, the faction whose turn is being crunched
    #             map - the grid which contains the tiles of the game
    #             map_size - the size of the map

    # visited 2D array keeps track of whether tile was visited or not
    visited = [[False] * map_size for _ in range(map_size)]

    # regions array keeps track of regions owned by the faction
    # a region being defined as an area of tiles owned by a faction which are all connected
    regions = []

    offset = 1
    for i in range(map_size):
        for j in range(map_size - offset):
            if (not visited[i][j]):
                if (map[i][j].owner == faction):
                    tiles, has_capital = BFS(map[i][j], visited, map)
                    region = SLRegion(faction, tiles, has_capital)
                    regions.append(region)
                else:
                    visited[i][j] = True
        if (offset == 1):
            offset = 0
        elif (offset == 0):
            offset = 1

    for id in faction.brigade_dict:
        movement.reset_moves(faction.brigade_dict[id], screen)

    for id in faction.building_dict:
        if (faction.building_dict[id].production > 0) and (faction.building_dict[id].health < faction.building_dict[id].max_health):
            faction.building_dict[id].health += 5
            if (faction.building_dict[id].health > faction.building_dict[id].max_health):
                faction.building_dict[id].health = max_health
            game_functions.reblit_tile(faction.building_dict[id].location, screen)

    faction.is_defeated = True

    for region in regions:
        apply_generation_and_attrition(region, screen)
        if (region.contains_capital):
            faction.is_defeated = False
