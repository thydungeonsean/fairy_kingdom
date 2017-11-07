from map_object import MapObject
from image_components.dummy_image_component import DummyImageComponent
from random import randint, choice
from src.constants import STUMP_L, STUMP_R


class House(MapObject):

    MUSHLOCK_THRESHOLD = 50
    HIBERNATE_POINT = 60

    RANDOM_PICK_CHANCE = 1
    SPEAR_CHANCE = 50

    def __init__(self, state, coord, start_food):

        MapObject.__init__(self, state, 'mushhouse', coord)
        self.coords = self.get_coords()
        self.blocks = True

        self.food = randint(0, 9) + start_food
        self.starvation = 0

        self.gems = 0

    def get_coords(self):
        ax, ay = self.coord
        bx, by = ax+1, ay
        return (ax, ay), (bx, by)

    def set_image_component(self):
        return DummyImageComponent()

    def destroy_house(self):

        l, r = self.get_coords()

        self.state.decay_map.add_decayable(l)
        self.state.decay_map.add_decayable(r)

        self.state.terrain_map.set_tile(l, STUMP_L)
        self.state.terrain_map.set_tile(r, STUMP_R)
        self.state.map_image.update((l, r))
        self.state.path_finding_map.compute()

        self.die()

        houses = self.state.object_list.get_all('mushhouse')
        self.state.object_list.houses_remain = len(houses) > 0
        self.state.score_keeper.subtract_house()

    def give_food(self):
        self.food += 10
        self.state.score_keeper.add_food()
        self.starvation = 0
        # call to any kind of global score thing

    def give_gem(self):
        self.gems += 1
        self.state.score_keeper.add_gem()
        self.food += 20
        self.starvation = 0
        # call to any kind of global score thing

    def run_house(self):

        self.starvation += 1
        if self.starvation < House.HIBERNATE_POINT:

            self.food += 1
            if self.food > House.MUSHLOCK_THRESHOLD:
                roll = randint(0, 99)

                if roll < self.food:
                    self.spawn_mushlock()

            if self.gems >= 1:
                self.spawn_tool()
            else:
                if randint(0, 99) < House.RANDOM_PICK_CHANCE:
                    coords = self.get_valid_spawn_coord()
                    if coords:
                        self.spawn_pick(coords)

    def spawn_mushlock(self):

        self.food = 0
        coords = self.get_valid_spawn_coord()
        if not coords:
            return
        else:
            self.state.object_creator.add_mushlock(choice(coords))

    def get_valid_spawn_coord(self):

        adj_to_house = set()
        for coord in self.get_coords():
            adj = self.state.terrain_map.get_passable_adj(coord)
            for point in adj:
                adj_to_house.add(point)

        return filter(lambda x: not self.state.object_list.point_is_blocked(x), adj_to_house)

    def spawn_tool(self):

        self.gems -= 1
        coords = self.get_valid_spawn_coord()
        if not coords:
            return

        if randint(0, 99) < House.SPEAR_CHANCE:
            self.spawn_spear(coords)
        else:
            self.spawn_pick(coords)

    def spawn_spear(self, coords):
        self.state.object_creator.add_spear(choice(coords))

    def spawn_pick(self, coords):

        self.state.object_creator.add_pick(choice(coords))

