

class Shroud(object):

    def __init__(self, state):

        self.state = state

        self.shroud = self.initialize_shroud()

    def initialize_shroud(self):

        shroud = set()
        for point in self.state.terrain_map.get_coord_list():
            shroud.add(point)

        return shroud

    def point_is_hidden(self, point):
        return point in self.shroud

    def explore(self, point):
        if self.point_is_hidden(point):
            self.shroud.remove(point)
            self.state.map_image.draw_tile(point)

    def explore_all(self):
        self.explore_list(self.state.terrain_map.get_coord_list())

    def explore_list(self, points):
        map(self.explore, points)
