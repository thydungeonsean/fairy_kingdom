from power import Power
from src.constants import *
from effects.flood_effect import FloodEffect


class River(Power):

    instance = None

    @classmethod
    def get_instance(cls):

        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):

        Power.__init__(self)

    def point_is_valid(self, point):
        return self.state.terrain_map.tile_is_horizontal_wall(point)

    def use_power(self, point):

        self.make_water_source(point)
        self.create_river(point)

    def make_water_source(self, point):

        self.state.terrain_map.set_tile(point, WATER_SOURCE)
        self.state.map_image.update([point])

    def create_river(self, (x, y)):

        first_point = (x, y+1)

        generator = self.state.river_generator

        river = generator.generate_single_river(first_point)

        flood_effect = FloodEffect(self.state, river)

        self.state.effect_handler.add_effect(flood_effect)



