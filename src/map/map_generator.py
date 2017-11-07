from terrain_map import TerrainMap
from src.constants import *
from random import *


class MapGenerator(object):

    WIDTH = MAP_W
    HEIGHT = MAP_H

    OPENING_CHANCE = 40

    DEATH_LIMIT = 4
    BIRTH_LIMIT = 3

    NUMBER_OF_PASSES = 2

    WATER_SPACING = 15

    ROCKINESS = .01
    HIDDEN_GEMS = 0.2
    REVEALED_GEMS = 0.007
    # REVEALED_GEMS = 0.05

    @classmethod
    def new_map(cls):

        return TerrainMap(cls.WIDTH, cls.HEIGHT)

    @classmethod
    def noise_map(cls):

        map = cls.new_map()

        for (x, y) in map.get_coord_list():
            if randint(0, 100) < cls.OPENING_CHANCE:
                map.set_tile((x, y), FLOOR)

        return map

    @classmethod
    def generate_cave_map(cls):

        cave_map = [[randint(0, 99) <= cls.OPENING_CHANCE for my in range(cls.HEIGHT)] for mx in range(cls.WIDTH)]

        for i in range(cls.NUMBER_OF_PASSES):

            cave_map = cls.run_cellular_automata(cave_map, cls.WIDTH, cls.HEIGHT)

        terrain_map = cls.new_map()
        for x, y in terrain_map.get_coord_list():
            if cave_map[x][y]:
                terrain_map.set_tile((x, y), FLOOR)

        cls.close_map_edge(terrain_map, cls.WIDTH, cls.HEIGHT)

        cls.add_water_sources(terrain_map)

        cls.add_rocks(terrain_map)

        return terrain_map

    @classmethod
    def run_cellular_automata(cls, prev_map, w, h):

        new_map = [[False for my in range(h)] for mx in range(w)]

        for y in range(h):
            for x in range(w):

                neighbours = cls.count_neighbours(prev_map, (x, y), w, h)

                if prev_map[x][y]:
                    if neighbours < cls.DEATH_LIMIT:
                        new_map[x][y] = False
                    else:
                        new_map[x][y] = True
                else:
                    if neighbours > cls.BIRTH_LIMIT:
                        new_map[x][y] = True
                    else:
                        new_map[x][y] = False

        return new_map

    @classmethod
    def count_neighbours(cls, cave_map, (px, py), w, h):

        count = 0

        for y in range(py - 1, py + 2):
            for x in range(px - 1, px + 2):
                if x < 0 or y < 0 or x >= w or y >= h:
                    pass
                elif cave_map[x][y]:
                    count += 1

        return count

    @classmethod
    def close_map_edge(cls, map, w, h):

        for x, y in map.get_coord_list():
            if x == 0 or x == w-1:
                map.set_tile((x, y), SOLID_WALL)
            elif y == 0 or y == h-1:
                map.set_tile((x, y), SOLID_WALL)

    @classmethod
    def add_water_sources(cls, terrain_map):

        potential_sources = filter(lambda x: cls.point_valid_water_source(terrain_map, x), terrain_map.get_coord_list())

        new_water_sources = []
        placed = 0
        while placed < 10 and potential_sources:

            new_water_sources.append(choice(potential_sources))
            potential_sources = filter(lambda x: cls.far_enough_from_sources(new_water_sources, x), potential_sources)
            placed += 1

        for point in new_water_sources:
            terrain_map.set_tile(point, WATER_SOURCE)

    @classmethod
    def point_valid_water_source(cls, terrain_map, (x, y)):
        point_below = (x, y+1)
        return terrain_map.get_tile((x, y)) in (WALL, SOLID_WALL) and terrain_map.point_in_bounds(point_below) \
            and terrain_map.tile_not_wall(point_below)

    @classmethod
    def far_enough_from_sources(cls, sources, (x, y)):

        for sx, sy in sources:
            if (abs(sx-x) + abs(sy-y)) < cls.WATER_SPACING:
                return False
        return True

    @classmethod
    def add_rocks(cls, terrain_map):

        rock_valid = terrain_map.get_all((FLOOR, GROWTH_1, GROWTH_2))
        num_rocks = int(len(rock_valid) * cls.ROCKINESS)

        points = sample(rock_valid, num_rocks)
        map(lambda x: terrain_map.set_tile(x, ROCK), points)

    @classmethod
    def place_hidden_gems(cls, terrain_map):

        gem_valid = terrain_map.get_all((ROCK, WALL))
        num_rocks = int(len(gem_valid) * cls.HIDDEN_GEMS)

        points = sample(gem_valid, num_rocks)
        return points

    @classmethod
    def place_revealed_gems(cls, terrain_map):

        gem_valid = terrain_map.get_all(FLOOR)
        num_rocks = int(len(gem_valid) * cls.REVEALED_GEMS)

        points = sample(gem_valid, num_rocks)
        return points
