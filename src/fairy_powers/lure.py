from power import Power


class Lure(Power):

    instance = None

    @classmethod
    def get_instance(cls):

        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):

        Power.__init__(self)

    def point_is_valid(self, point):
        passable = self.state.terrain_map.point_is_passable(point)
        clear = not self.state.object_list.point_is_blocked(point)
        no_lure = len(filter(lambda x: x.coord == point, self.state.object_list.get_all('lure'))) == 0

        return passable and clear and no_lure

    def use_power(self, point):

        self.state.object_creator.add_lure(point)
