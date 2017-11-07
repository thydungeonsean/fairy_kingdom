from power import Power
from src.constants import HOUSE_L, HOUSE_R, ROCK


class Rock(Power):

    instance = None

    @classmethod
    def get_instance(cls):

        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):

        Power.__init__(self)

    def point_is_valid(self, point):

        crushable = self.state.terrain_map.point_is_crushable(point)

        return crushable

    def use_power(self, point):
        self.crush_house(point)
        self.add_rock(point)
        self.crush_point(point)

    def crush_house(self, point):
        if self.state.terrain_map.get_tile(point) in (HOUSE_L, HOUSE_R):
            house = filter(lambda x: point in x.get_coords(), self.state.object_list.get_all('mushhouse'))
            assert len(house) == 1
            house[0].destroy_house()

    def crush_point(self, point):

        stopped_water = self.state.object_list.get_all_of_key_at_coord('water', point)
        if stopped_water:
            self.obstruct_river(point)

        orcs = self.state.object_list.get_all_of_key_at_coord('orc', point)
        for orc in orcs:
            orc.ai_component.health = 0
            orc.die()
        mushlocks = self.state.object_list.get_all_of_key_at_coord('mushlock', point)
        for mushlock in mushlocks:
            mushlock.ai_component.health = 0
            mushlock.die()

        # destroy all other objects
        crushed = self.state.object_list.get_objects_at_coord(point)
        map(lambda x: x.die(), crushed)
        self.state.plant_map.clear_plant(point)

    def add_rock(self, point):

        self.state.terrain_map.set_tile(point, ROCK)
        self.state.map_image.update((point,))
        self.state.path_finding_map.compute()

    def obstruct_river(self, point):

        water = filter(lambda x: x.coord == point, self.state.object_list.get_all('water'))
        for w in water:
            river = w.river
            river.block_river(point)
