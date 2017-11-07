from src.constants import *
from random import *
from src.actor.plant import Plant


class MapAutomata(object):

    LUSHNESS = 10
    GROWTH_DIE_CHANCE = 4
    SPREAD_CHANCE = 3
    DIE_LEVEL = 3

    grow_table = {GROWTH_1: GROWTH_2, GROWTH_2: GROWTH_3, GROWTH_3: GROWTH_3}
    die_table = {GROWTH_1: FLOOR, GROWTH_2: GROWTH_1, GROWTH_3: GROWTH_2}

    def __init__(self, state, terrain_map):

        self.state = state
        self.terrain_map = terrain_map
        self.changed = set()

    def initial_automata(self):

        self.make_river_beds()

        self.make_river_banks()

        for i in range(MapAutomata.LUSHNESS):
            self.run_growth_automata()
            self.spread_growth()

        self.find_starting_area()

        self.produce_crops()

        self.update_map_image()

    def run(self):

        self.produce_crops()
        self.run_growth_automata()
        self.spread_growth()

        self.update_map_image()

    def get_river_tiles(self):

        return map(lambda x: x.coord, self.state.object_list.get_all('water'))

    def get_gem_tiles(self):
        return map(lambda x: x.coord, self.state.object_list.get_all('gem'))

    def make_river_beds(self):

        for point in self.get_river_tiles():
            if self.terrain_map.get_tile(point) != GROWTH_3:
                self.terrain_map.set_tile(point, GROWTH_3)
                self.change_tile(point)

    def change_tile(self, point):
        self.changed.add(point)

    def update_map_image(self):

        self.state.map_image.update(self.changed)
        self.changed = set()

    def make_river_banks(self):

        for point in self.get_river_tiles():
            adj = self.get_adj(point)
            for a in adj:
                if self.terrain_map.get_tile(a) == FLOOR:
                    if randint(0, 99) < 75:
                        new_tile = GROWTH_1
                    else:
                        new_tile = GROWTH_2
                    self.terrain_map.set_tile(a, new_tile)
                    self.change_tile(a)

    def get_adj(self, (x, y)):

        return (x-1, y), (x+1, y), (x, y-1), (x, y+1)

    def run_growth_automata(self):

        river = set(self.get_river_tiles())

        growth_1_list = self.terrain_map.get_all(GROWTH_1)
        growth_2_list = self.terrain_map.get_all(GROWTH_2)
        growth_3_list = filter(lambda x: x not in river, self.terrain_map.get_all(GROWTH_3))

        grow_list = []
        die_list = []

        i = 1
        for group in (growth_3_list, growth_2_list, growth_1_list):
            grow, die = self.grow_group(group, i, river)
            grow_list.extend(grow)
            die_list.extend(die)
            i += 1

        for point in grow_list:
            self.grow_point(point)
        for point in die_list:
            self.die_point(point)

    def grow_point(self, point):
        current = self.terrain_map.get_tile(point)
        assert current in (GROWTH_1, GROWTH_2, GROWTH_3)
        cls = MapAutomata
        self.terrain_map.set_tile(point, cls.grow_table[current])
        self.change_tile(point)

    def die_point(self, point):
        current = self.terrain_map.get_tile(point)
        assert current in (GROWTH_1, GROWTH_2, GROWTH_3)
        cls = MapAutomata
        self.terrain_map.set_tile(point, cls.die_table[current])
        self.change_tile(point)

    def grow_group(self, group, level, river):

        grow = []
        die = []

        for point in group:

            score, watered = self.get_growth_score(point, river)
            score += level - MapAutomata.GROWTH_DIE_CHANCE
            if watered:
                die_chance = MapAutomata.DIE_LEVEL - randint(0, MapAutomata.DIE_LEVEL+1)
            else:
                die_chance = MapAutomata.DIE_LEVEL
            if randint(0, 9) < die_chance:
                die.append(point)
            else:
                if randint(0, 9) < score:
                    grow.append(point)
        return grow, die

    def get_growth_score(self, (x, y), river):

        adj = self.get_adj((x, y))
        watered = False
        score = 0
        for a in adj:
            if a in river:
                score += 2
                watered = True
            elif self.terrain_map.get_tile(a) == GROWTH_3:
                score += 2
            elif self.terrain_map.get_tile(a) in (GROWTH_1, GROWTH_2):
                score += 1
        return score, watered

    def spread_growth(self):

        river = set(self.get_river_tiles())

        growth_1_list = self.terrain_map.get_all(GROWTH_1)
        growth_2_list = self.terrain_map.get_all(GROWTH_2)
        growth_3_list = filter(lambda x: x not in river, self.terrain_map.get_all(GROWTH_3))

        for point in river:
            self.spread_river_bed(point)

        i = 1
        for group in (growth_3_list, growth_2_list, growth_1_list):
            self.spread_group(group, i)
            i += 1

    def spread_group(self, group, level):

        for point in group:

            self.spread_point(point, level)

    def spread_point(self, point, level):
        cls = MapAutomata

        if randint(0, 9) < level+cls.SPREAD_CHANCE:
            self.try_to_spread(point)

    def try_to_spread(self, point):

        adj = self.get_adj(point)
        a = choice(adj)
        if self.terrain_map.get_tile(a) == FLOOR:
            self.terrain_map.set_tile(a, GROWTH_1)
            self.change_tile(a)

    def spread_river_bed(self, point):

        adj = self.get_adj(point)
        for a in adj:
            if self.terrain_map.get_tile(a) == FLOOR:
                self.terrain_map.set_tile(a, GROWTH_1)
                self.change_tile(a)

    def produce_crops(self):

        river = set(self.get_river_tiles())
        gem = set(self.get_gem_tiles())
        plants = set(map(lambda x: x.coord, self.state.object_list.get_all(PLANT)))
        blocked = river.union(gem.union(plants))

        growth_1_list = filter(lambda x: self.no_plant_here(x, blocked), self.terrain_map.get_all(GROWTH_1))
        growth_2_list = filter(lambda x: self.no_plant_here(x, blocked), self.terrain_map.get_all(GROWTH_2))
        growth_3_list = filter(lambda x: self.no_plant_here(x, blocked), self.terrain_map.get_all(GROWTH_3))

        i = 1
        for group in (growth_3_list, growth_2_list, growth_1_list):
            for point in group:
                self.produce_plant(point, i)
            i += 1

    def no_plant_here(self, point, plants):
        return point not in plants

    def produce_plant(self, point, level):

        if randint(0, 99) < level*3:
            self.state.object_creator.add_plant(point)

    def find_starting_area(self):

        coords = set(self.terrain_map.get_all(FLOOR))
        water = self.terrain_map.get_all(WATER_SOURCE)
        near_water = self.get_coords_near_water(self.terrain_map, coords, water)
        near_water = list(near_water)
        shuffle(near_water)

        found = False

        for point in near_water:
            if self.good_start_point(point):
                self.create_start_area(point)
                found = True
                break

        # TODO brute force a start point
        if not found:
            raise Exception('no good start point found')

    @staticmethod
    def get_coords_near_water(terrain, floor, water):

        near_water = set()
        for wx, wy in water:
            for y in range(wy - 10, wy + 11):
                for x in range(wx - 10, wx + 11):
                    if terrain.point_in_bounds((x, y)):
                        near_water.add((x, y))

        valid = near_water.intersection(floor)
        return valid

    def good_start_point(self, (sx, sy)):

        river = set(self.get_river_tiles())
        walls = set(self.terrain_map.get_all(WALL))
        walls = walls.union(self.terrain_map.get_all(SOLID_WALL))

        blocked = walls.union(river)

        area = self.get_area((sx, sy))

        return not area.intersection(blocked)

    def get_area(self, (sx, sy)):
        area = set()
        for x in range(sx - 1, sx + 3):
            for y in range(sy - 3, sy + 2):
                area.add((x, y))
        return area

    def create_start_area(self, point):

        self.state.view.set_start_area(point)

        area = list(self.get_area(point))
        for p in area:
            self.terrain_map.set_tile(p, FLOOR)
            self.change_tile(p)

        x, y = point
        self.state.object_creator.add_house(point)
        a = x-1, y
        b = x+2, y
        c = x, y+1
        d = x+1, y+1
        self.state.object_creator.add_mushlock(a)
        self.state.object_creator.add_mushlock(b)
        self.state.object_creator.add_mushlock(c)
        self.state.object_creator.add_mushlock(d)

