from behaviour import Behaviour
from random import choice, shuffle, randint


class Destroy(Behaviour):

    BLOOD_LUST_LEVEL = 80

    def __init__(self):

        Behaviour.__init__(self)

    def run_specifics(self):

        if self.at_house():
            self.destroy_house()
            return

        adj = self.get_assault_adj()
        values = {}
        for point in adj:
            value = self.find_attack_path_value(point)
            if value is not None:
                values[point] = value

        if not values:
            self.ai_component.use_action()
            return

        move = self.find_best_move(values)
        self.actor.assault(move)
        self.ai_component.use_action()

    @property
    def house_map(self):
        return self.actor.state.path_finding_map.return_map

    def at_house(self):
        return self.house_map.get(self.actor.coord) == 1

    def find_attack_path_value(self, point):
        return self.find_pathing_value(self.house_map, point)

    def destroy_house(self):

        house = choice(self.get_adj_houses())
        house.destroy_house()
        self.actor.state.mushlock_ai_overlord.mushhouse_pillaged()
        self.ai_component.use_action(6)

        self.ai_component.rage -= randint(0, 100)

    def get_adj_houses(self):
        houses = self.actor.state.object_list.get_all('mushhouse')
        adj = set(self.get_adj())
        adj_houses = []
        for house in houses:
            house_coords = set(house.get_coords())
            if house_coords.intersection(adj):
                adj_houses.append(house)
        return adj_houses

    def get_assault_adj(self):

        adj = self.actor.state.terrain_map.get_passable_adj(self.actor.coord)

        blockers = self.actor.state.object_list.get_blockers()
        non_mushlock = filter(lambda x: x.key != 'mushlock', blockers)

        blocked_coords = set(map(lambda x: x.coord, non_mushlock))

        for point in adj[:]:

            if point in blocked_coords:
                adj.remove(point)
                continue

        return adj
