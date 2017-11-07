from src.constants import *


class TerrainMap(object):

    PASSABLE = FLOOR, GROWTH_1, GROWTH_2, GROWTH_3, RUBBLE
    CRUSHABLE = FLOOR, GROWTH_1, GROWTH_2, GROWTH_3, STUMP, STUMP_L, STUMP_R, HOUSE_L, HOUSE_R
    MINABLE = ROCK, WALL, STUMP, STUMP_R, STUMP_L

    def __init__(self, w, h):

        self.state = None

        self.w = w
        self.h = h
        self.tiles = [[WALL for my in range(h)] for mx in range(w)]

    def bind_state(self, state):
        self.state = state

    def set_tile(self, (x, y), value):
        assert self.point_in_bounds((x, y))
        self.tiles[x][y] = value
        
    def point_in_bounds(self, (x, y)):
        return 0 <= x < self.w and 0 <= y < self.h

    def get_tile(self, (x, y)):
        assert self.point_in_bounds((x, y))
        return self.tiles[x][y]

    def get_coord_list(self):

        coords = []

        for y in range(self.h):
            for x in range(self.w):
                coords.append((x, y))

        return coords

    def tile_not_wall(self, (x, y)):
        return self.get_tile((x, y)) not in (WALL, SOLID_WALL, WATER_SOURCE)

    def tile_blocks_water(self, (x, y)):
        return self.get_tile((x, y)) in (WALL, SOLID_WALL, WATER_SOURCE, ROCK)

    def tile_is_horizontal_wall(self, (x, y)):
        wall = self.get_tile((x, y)) in (WALL, SOLID_WALL)
        point_below = (x, y+1)
        return wall and self.point_in_bounds(point_below) and self.tile_not_wall(point_below)

    def get_all(self, of_type):
        if isinstance(of_type, int):
            return filter(lambda x: self.get_tile(x) == of_type, self.get_coord_list())
        else:
            return filter(lambda x: self.get_tile(x) in of_type, self.get_coord_list())

    def add_house(self, (x, y)):
        a = (x, y)
        b = (x+1, y)
        self.set_tile(a, HOUSE_L)
        self.set_tile(b, HOUSE_R)
        self.state.path_finding_map.compute()

        self.state.map_image.update((a, b))

    def get_adj(self, (x, y)):

        return filter(self.point_in_bounds, [(x-1, y), (x+1, y), (x, y-1), (x, y+1)])

    def get_passable_adj(self, (x, y)):
        adj = self.get_adj((x, y))
        return filter(self.point_is_passable, adj)

    def point_is_passable(self, point):
        return self.get_tile(point) in TerrainMap.PASSABLE

    def point_is_crushable(self, point):
        return self.get_tile(point) in TerrainMap.CRUSHABLE

    def point_is_minable(self, point):
        return self.get_tile(point) in TerrainMap.MINABLE

    def mine_point(self, (x, y)):

        self.set_tile((x, y), FLOOR)

        self.state.path_finding_map.compute()
        self.state.map_image.make_rubble((x, y))

        self.reveal_gem((x, y))
        self.kill_mark((x, y))

    def reveal_gem(self, point):
        hidden = filter(lambda x: x.coord == point, self.state.object_list.get_all('gem'))
        if hidden:
            hidden[0].discover_gem()

    def kill_mark(self, point):
        mark = filter(lambda x: x.coord == point, self.state.object_list.get_all('mark'))
        if mark:
            mark[0].kill_mark()

