from behaviour import Behaviour
from random import shuffle, choice


class Return(Behaviour):

    def __init__(self):
        Behaviour.__init__(self)

    def run_specifics(self):

        if self.at_house():
            if self.ai_component.has_food:
                self.drop_off_food()
                return
            elif self.ai_component.has_gem:
                self.drop_off_gem()
                return

        adj = self.get_passable_adj()
        values = {}
        for point in adj:
            value = self.find_return_path_value(point)
            if value is not None:
                values[point] = value

        if not values:
            # we can't return
            self.actor.drop()
            self.ai_component.use_action()
            return

        move = self.find_best_move(values)
        self.actor.move(move)
        self.ai_component.use_action()

    @property
    def return_map(self):
        return self.actor.state.path_finding_map.return_map

    def find_return_path_value(self, point):
        return self.find_pathing_value(self.return_map, point)

    def at_house(self):
        return self.return_map.get(self.actor.coord) == 1

    def drop_off_food(self):

        # find an adjacent house
        houses = self.get_adj_house()

        if houses:
            choice(houses).give_food()
        else:
            self.actor.drop()
            raise Exception('tried to give food -- no house?')

        self.actor.drop()
        self.ai_component.use_action()

    def get_adj_house(self):
        houses = self.actor.state.object_list.get_all('mushhouse')
        adj = set(self.get_adj())
        adj_houses = []
        for house in houses:
            house_coords = set(house.get_coords())
            if house_coords.intersection(adj):
                adj_houses.append(house)
        return adj_houses

    def drop_off_gem(self):
        houses = self.get_adj_house()

        if houses:
            choice(houses).give_gem()
        else:
            raise Exception('tried to give food -- no house?')

        self.actor.drop()
        self.ai_component.use_action()
