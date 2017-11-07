from behaviour import Behaviour
from random import choice
from random import randint
from random import shuffle


class Wander(Behaviour):

    WANT_TO_HOUSE_CHANCE = 30

    def __init__(self):

        Behaviour.__init__(self)

    def run_specifics(self):

        possible_moves = self.get_passable_adj()

        adj_lures = self.find_lures(possible_moves)
        adj_food = self.find_food(possible_moves)
        adj_gems = self.find_gems(possible_moves)
        adj_to_sleeper = self.find_sleeper(possible_moves)
        if adj_lures:
            possible_moves = adj_lures
        elif adj_gems:
            possible_moves = adj_gems
        elif adj_food:
            possible_moves = adj_food
        elif adj_to_sleeper and self.ai_component.fatigue > 25 and randint(0, 99) < Wander.WANT_TO_HOUSE_CHANCE:
            possible_moves = adj_to_sleeper
        else:
            possible_moves.append(self.actor.coord)

        lure_approach = self.try_lure_map(possible_moves)
        if lure_approach:
            move = self.find_best_move(lure_approach)
            self.actor.move(move)
            self.ai_component.use_action()
        else:
            move = choice(possible_moves)
            self.actor.move(move)
            self.ai_component.use_action()

    def try_lure_map(self, adj):

        values = {}
        for point in adj:
            value = self.find_lure_path_value(point)
            if value is not None:
                values[point] = value

        return values

    @property
    def lure_map(self):
        return self.actor.state.path_finding_map.lure_map

    def find_lure_path_value(self, point):
        return self.find_pathing_value(self.lure_map, point)
