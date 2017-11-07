from effect import Effect
from src.constants import *


class FloodEffect(Effect):

    FLOOD_SPEED = 2

    def __init__(self, state, river, start_index=0):

        Effect.__init__(self, None)

        self.state = state
        self.river = river
        self.river_points = river.river_points
        self.current_index = start_index

    def initialize_tick(self):
        return 0

    def initialize_speed(self):
        return FloodEffect.FLOOD_SPEED

    def run_effect(self):

        if self.current_index >= len(self.river_points):
            self.create_river_bed()
            self.die()

        else:

            self.flood_point()

    def flood_point(self):

        point = self.river_points[self.current_index]

        self.state.object_creator.add_water(point, self.river)
        self.purge_point(point)

        self.current_index += 1

    def create_river_bed(self):

        for point in self.river_points:
            self.state.terrain_map.set_tile(point, GROWTH_3)

        self.state.map_image.update(self.river_points)

    def purge_point(self, point):

        obstructing_actors = filter(lambda x: x.coord == point,
                                    self.state.object_list.get_all(('orc', 'mushlock', PLANT)))
        map(lambda x: x.die(), obstructing_actors)

        houses = filter(lambda x: point in x.get_coords(), self.state.object_list.get_all('mushhouse'))
        for house in houses:
            house.destroy_house()
