from src.actor.mushlock import Mushlock
from src.actor.house import House
from src.actor.plant import Plant
from src.actor.lure import Lure
from random import shuffle, choice
from src.constants import PLANT, STUMP
from src.actor.water import Water
from src.actor.orc import Orc
from src.actor.mark import Mark
from src.actor.gem import Gem
from src.actor.pick import Pick
from src.actor.spear import Spear
from src.constants import MAX_MUSHLOCKS


class ObjectCreator(object):

    def __init__(self, state):

        self.state = state
        self.mushlocks = 4

    def add_house(self, point, start_food=0):

        self.state.score_keeper.add_house()

        self.state.object_list.add_object(House(self.state, point, start_food))
        self.state.terrain_map.add_house(point)

    def add_mushlock(self, point):
        if self.mushlocks >= MAX_MUSHLOCKS:
            pass
        else:
            self.state.score_keeper.add_mushlock()
            self.mushlocks += 1
            mushlock = Mushlock(self.state, point)
            mushlock.explore()
            self.state.object_list.add_object(mushlock)

    def add_orc(self, point):
        orc = Orc(self.state, point)
        self.state.object_list.add_object(orc)

    def add_lure(self, point):
        lure = Lure(self.state, point)
        self.state.object_list.add_object(lure)
        self.state.path_finding_map.compute_lure_map()

    def add_mark(self, point):
        mark = Mark(self.state, point)
        self.state.object_list.add_object(mark)
        self.state.path_finding_map.compute_mark_map()

    def add_gem(self, point):
        gem = Gem(self.state, point)
        self.state.object_list.add_object(gem)

    def add_plant(self, point):
        self.state.plant_map.add_plant(point)

    def add_water(self, point, river):
        self.state.object_list.add_object(Water(self.state, river, point))

    def add_pick(self, point):
        pick = Pick(self.state, point)
        self.state.object_list.add_object(pick)

    def add_spear(self, point):
        spear = Spear(self.state, point)
        self.state.object_list.add_object(spear)

    def spawn_new_houses(self):

        mushlocks = self.state.object_list.get_all('mushlock')
        sleepers = filter(lambda x: x.sleeping, mushlocks)
        shuffle(sleepers)

        for i in range(len(sleepers)):
            sleeper_a = sleepers.pop()
            x, y = sleeper_a.coord
            adj = (x-1, y), (x+1, y)

            house_partner = filter(lambda x: x.coord in adj, sleepers)
            if house_partner:
                sleeper_b = choice(house_partner)

                leftmost = sorted([sleeper_a.coord, sleeper_b.coord], key=lambda l: l[0])[0]

                if self.water_in_way(leftmost):
                    continue

                self.spawn_new_house(sleeper_a, sleeper_b, leftmost)
                return

    def spawn_new_house(self, a, b, leftmost):

        a.die()
        b.die()

        self.clear_points((a.coord, b.coord))

        self.add_house(leftmost, start_food=45)
        self.state.object_list.houses_remain = True

    def water_in_way(self, (x, y)):

        points = {(x, y), (x+1, y)}
        water = set(map(lambda x: x.coord, self.state.object_list.get_all('water')))

        return points.intersection(water)

    def clear_points(self, points):

        for point in points:
            self.state.plant_map.clear_plant(point)

    def stumpify(self, mush):

        point = mush.coord
        water = self.state.object_list.get_all_of_key_at_coord('water', point)
        if not water:
            self.state.terrain_map.set_tile(point, STUMP)
            self.state.map_image.update((point,))
            self.state.plant_map.clear_plant(point)
