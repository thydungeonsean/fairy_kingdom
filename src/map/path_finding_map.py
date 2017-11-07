from src.constants import *


class PathFindingMap(object):

    PASSABLE = FLOOR, GROWTH_1, GROWTH_2, GROWTH_3

    LURE_FORCE = 8
    MARK_FORCE = 8

    def __init__(self, state, terrain_map):

        self.state = state
        self.terrain_map = terrain_map

        self.return_map = None
        self.lure_map = None
        self.mark_map = None

    def compute(self):

        self.compute_house_map()
        self.compute_lure_map()
        self.compute_mark_map()

    def compute_house_map(self):
        houses = self.terrain_map.get_all((HOUSE_L, HOUSE_R))
        self.return_map = self.get_dijkstra(houses)

    def compute_lure_map(self):

        lures = map(lambda x: x.coord, self.state.object_list.get_all('lure'))
        self.lure_map = self.get_dijkstra(lures, limit=PathFindingMap.LURE_FORCE)

    def compute_mark_map(self):

        marks = map(lambda x: x.coord, self.state.object_list.get_all('mark'))
        self.mark_map = self.get_dijkstra(marks, limit=PathFindingMap.MARK_FORCE)

    def get_next_edge(self, edge):

        next_edge = set()

        for point in edge:
            adj = self.terrain_map.get_adj(point)
            for a in adj:
                next_edge.add(a)
        return list(next_edge)

    def get_dijkstra(self, edge, limit=None):

        d_map = {}

        touched = set()
        value = 0

        while edge:
            for point in edge:
                touched.add(point)
                if d_map.get(point) is None:
                    d_map[point] = value
                elif value < d_map.get(point):
                    d_map[point] = value

            next_edge = self.get_next_edge(edge)
            edge = list(filter(lambda x: self.tile_passable(x) and x not in touched, next_edge))

            value += 1
            if limit is not None and value > limit:
                break

        return d_map

    def tile_passable(self, point):
        return self.terrain_map.get_tile(point) in PathFindingMap.PASSABLE
