from src.constants import *
from random import randint, choice
from src.fairy_powers.effects.flood_effect import FloodEffect


class River(object):

    RIVER_SIZE = 10

    def __init__(self, state, start_point, instant=False):

        self.state = state
        self.terrain_map = state.terrain_map
        self.start_point = start_point

        self.river_points = []

        self.generate_river(instant=instant)

    def generate_river(self, instant=False):

        self.river_points = self.generate_river_path([self.start_point])
        if instant:
            self.instant_flood_river(self.river_points)

    def generate_river_path(self, river):

        cls = River

        while True:
            river_edge = river[-1]
            next_point = self.get_next_river_point(river, river_edge, long_enough=len(river) >= cls.RIVER_SIZE)
            if not next_point:
                break
            elif self.terrain_map.tile_blocks_water(next_point):
                break
            else:
                river.append(next_point)

        return river

    def get_next_river_point(self, river, (x, y), long_enough=False):

        possible = {'down': (x, y+1), 'left': (x-1, y), 'right': (x+1, y)}
        for key in possible.keys():
            if possible[key] in river:
                del possible[key]
            elif not long_enough and self.terrain_map.tile_blocks_water(possible[key]):
                del possible[key]
            elif self.tile_is_surrounded_with_water(river, possible[key]):
                del possible[key]

        if len(possible) == 3:
            roll = randint(0, 99)
            if roll < 70:
                return possible['down']
            elif roll < 85:
                return possible['left']
            else:
                return possible['right']
        elif len(possible) > 0:
            return choice(possible.values())
        else:
            return False

    @staticmethod
    def tile_is_surrounded_with_water(river, (x, y)):

        adj = ((x-1, y), (x+1, y), (x, y-1), (x, y+1))
        count = 0
        for a in adj:
            if a in river:
                count += 1
        return count > 1

    def add_water(self, point):
        self.state.object_creator.add_water(point, self)

    def instant_flood_river(self, river):
        for point in river:
            self.add_water(point)

    def block_river(self, point):

        i = self.river_points.index(point)
        dry_path = self.river_points[i:]
        self.river_points = self.river_points[:i]
        self.dry_part_of_river(dry_path)

        self.try_to_divert_river()

    def dry_part_of_river(self, points):
        waters = self.state.object_list.get_all('water')
        for point in points:
            tiles = filter(lambda x: x.coord == point and x.river == self, waters)
            for tile in tiles:
                tile.die()

    def try_to_divert_river(self):

        if not self.river_points:  # we blocked it at the source
            return

        self.divert_river()

    def divert_river(self):

        i = len(self.river_points)
        self.river_points = self.generate_river_path(self.river_points)

        flood_effect = FloodEffect(self.state, self, start_index=i)
        self.state.effect_handler.add_effect(flood_effect)
