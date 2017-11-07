from power import Power


class Mark(Power):

    instance = None

    @classmethod
    def get_instance(cls):

        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):

        Power.__init__(self)

    def point_is_valid(self, point):
        minable = self.state.terrain_map.point_is_minable(point)
        no_mark = len(filter(lambda x: x.coord == point, self.state.object_list.get_all('mark'))) == 0

        return minable and no_mark

    def use_power(self, point):

        self.state.object_creator.add_mark(point)
