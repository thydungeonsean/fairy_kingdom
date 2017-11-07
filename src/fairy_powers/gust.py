from power import Power
from src.fairy_powers.effects.gust_effect import GustEffect


class Gust(Power):

    instance = None

    @classmethod
    def get_instance(cls):

        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):

        Power.__init__(self)
        self.gust_targets = None

    def point_is_valid(self, point):
        passable = self.state.terrain_map.point_is_passable(point)
        self.gust_targets = self.get_valid_targets(point)
        targets = len(self.gust_targets) > 0
        return passable and targets

    def use_power(self, point):
        for target in self.gust_targets:
            self.assign_gust_effect(target, point)
            target.ai_component.use_action(5)

        self.gust_targets = None

    def get_valid_targets(self, point):

        adj = set(self.state.terrain_map.get_adj(point))
        adj_targets = filter(lambda x: x.coord in adj, self.state.object_list.get_all(('mushlock', 'orc')))
        point_target_dict = {target.coord: target for target in adj_targets}
        adj_targets = self.somewhere_to_go(point, point_target_dict)
        return adj_targets

    def somewhere_to_go(self, (x, y), point_target_dict):

        have_somewhere_to_go = []

        point_to_next_point = {
            (x-1, y): (x-2, y),
            (x+1, y): (x+2, y),
            (x, y-1): (x, y-2),
            (x, y+1): (x, y+2),
        }

        for point, target in point_target_dict.iteritems():
            next_point = point_to_next_point[point]
            if self.state.terrain_map.point_is_passable(next_point) and \
                    not self.state.object_list.point_is_blocked(next_point):
                have_somewhere_to_go.append(target)

        return have_somewhere_to_go

    def assign_gust_effect(self, target, (ox, oy)):
        tx, ty = target.coord

        vx = tx-ox
        vy = ty-oy

        vector = (vx, vy)
        effect = GustEffect(target, vector)
        self.state.effect_handler.add_effect(effect)
