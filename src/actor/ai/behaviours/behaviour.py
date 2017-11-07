from src.constants import *
from random import shuffle


class Behaviour(object):

    def __init__(self):

        self.actor = None
        self.ai_component = None

    def run_behaviour(self, ai_component):

        self.ai_component = ai_component
        self.actor = ai_component.owner

        self.run_specifics()

        self.actor = None
        self.ai_component = None

    def run_specifics(self):
        raise NotImplementedError

    def get_adj(self):

        x, y = self.actor.coord
        adj = [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
        return adj

    def get_passable_adj(self):

        adj = self.actor.state.terrain_map.get_passable_adj(self.actor.coord)

        object_list = self.actor.state.object_list

        for point in adj[:]:

            if object_list.point_is_blocked(point):
                adj.remove(point)
                continue

        return adj

    def find_lures(self, adj):

        lures = map(lambda x: x.coord, self.actor.state.object_list.get_all('lure'))
        return list(set(lures).intersection(set(adj)))

    def find_food(self, adj):

        return filter(self.actor.state.plant_map.get_plant, adj)

    def find_sleeper(self, moves):
        moves.append(self.actor.coord)
        adj_points = {}
        for x, y in moves:
            adj_points[(x-1, y)] = (x, y)
            adj_points[(x+1, y)] = (x, y)

        sleepers = map(lambda x: x.coord, filter(lambda x: x.sleeping,
                                                 self.actor.state.object_list.get_all('mushlock')))
        adj_sleepers = list(set(adj_points.keys()).intersection(set(sleepers)))
        return map(lambda x: adj_points[x], adj_sleepers)

    def find_gems(self, adj):

        gems = map(lambda x: x.coord, self.actor.state.object_list.get_all('gem'))
        return list(set(gems).intersection(set(adj)))

    def find_best_move(self, values):

        keys = values.keys()
        shuffle(keys)
        weighted = sorted(keys, key=lambda x: values[x])

        return weighted[0]

    def find_pathing_value(self, d_map, point):
        return d_map.get(point, None)

    def get_minable_adj(self):
        map = self.actor.state.terrain_map
        return filter(lambda x: map.point_is_minable(x), map.get_adj(self.actor.coord))
