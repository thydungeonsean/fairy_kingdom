from power import Power


class Sleep(Power):

    instance = None

    @classmethod
    def get_instance(cls):

        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):

        Power.__init__(self)

    def point_is_valid(self, point):
        mushlock_coords = set(map(lambda x: x.coord, self.state.object_list.get_all('mushlock')))
        return point in mushlock_coords

    def use_power(self, point):
        self.sleep_spell(point)

    def sleep_spell(self, coord):
        mushlocks = self.state.object_list.get_all('mushlock')
        target = filter(lambda x: x.coord == coord, mushlocks)[0]
        target.tire_out()
