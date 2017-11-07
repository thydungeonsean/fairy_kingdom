from power import Power


class See(Power):

    instance = None

    @classmethod
    def get_instance(cls):

        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):

        Power.__init__(self)

    def use_power(self, point):

        sight = self.get_patch(point)

        self.state.shroud.explore_list(sight)
        self.reveal_hidden_gems(sight)

    def get_patch(self, (x, y)):

        patch = [
                                (x-1, y+3), (x, y+3), (x+1, y+3),
                    (x-2, y+2), (x-1, y+2), (x, y+2), (x+1, y+2), (x+2, y+2),
        (x-3, y+1), (x-2, y+1), (x-1, y+1), (x, y+1), (x+1, y+1), (x+2, y+1), (x+3, y+1),
        (x - 3, y), (x - 2, y), (x - 1, y), (x, y), (x + 1, y), (x + 2, y), (x + 3, y),
        (x - 3, y-1), (x - 2, y-1), (x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x + 2, y - 1), (x + 3, y -1),
                    (x - 2, y - 2), (x - 1, y - 2), (x, y - 2), (x + 1, y - 2), (x + 2, y - 2),
                                 (x - 1, y - 3), (x, y - 3), (x + 1, y - 3),
        ]

        return filter(self.state.terrain_map.point_in_bounds, patch)

    def reveal_hidden_gems(self, sight):

        sight = set(sight)

        gems = filter(lambda x: x.coord in sight, self.state.object_list.get_all('gem'))
        for gem in gems:
            if gem.hidden:
                gem.reveal_gem()

