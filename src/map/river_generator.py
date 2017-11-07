from random import *
from src.constants import *
from river import River


class RiverGenerator(object):

    RIVER_SIZE = 10

    def __init__(self, state, terrain_map):

        self.state = state
        self.terrain_map = terrain_map

        self.generate_rivers()

    def generate_rivers(self):

        sources = self.terrain_map.get_all(WATER_SOURCE)

        for (x, y) in sources:
            river_start = (x, y+1)
            River(self.state, river_start, instant=True)

    def generate_single_river(self, start):
        return River(self.state, start)
