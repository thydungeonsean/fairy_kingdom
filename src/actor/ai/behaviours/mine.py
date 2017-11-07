from wander import Wander
from random import choice, randint


class Mine(Wander):

    RANDOM_MINE_CHANCE = 1

    def __init__(self):
        Wander.__init__(self)

    def run_specifics(self):

        if self.try_to_mine():
            self.ai_component.use_action(5)
            return

        possible_moves = self.get_passable_adj()

        adj_lures = self.find_lures(possible_moves)
        adj_gems = self.find_gems(possible_moves)

        if adj_lures:
            possible_moves = adj_lures
        elif adj_gems:
            self.actor.drop_pick()
            possible_moves = adj_gems
        else:
            possible_moves.append(self.actor.coord)

        approach_mark = self.try_mark_map(possible_moves)
        approach_lure = self.try_lure_map(possible_moves)
        if approach_mark:
            move = self.find_best_move(approach_mark)
            self.actor.move(move)
            self.ai_component.use_action()
        elif approach_lure:
            move = self.find_best_move(approach_lure)
            self.actor.move(move)
            self.ai_component.use_action()
        else:
            move = choice(possible_moves)
            self.actor.move(move)
            self.ai_component.use_action()

    def try_mark_map(self, adj):

        values = {}
        for point in adj:
            value = self.find_mark_path_value(point)
            if value is not None:
                values[point] = value

        return values

    @property
    def mark_map(self):
        return self.actor.state.path_finding_map.mark_map

    def find_mark_path_value(self, point):
        return self.find_pathing_value(self.mark_map, point)

    def try_to_mine(self):

        minable = set(self.get_minable_adj())
        if minable:
            marked_points = set(map(lambda x: x.coord, self.actor.state.object_list.get_all('mark')))

            marked_targets = list(minable.intersection(marked_points))
            if marked_targets:
                # then mine a marked wall/rock
                self.mine(choice(marked_targets))
                return True
            else:
                if randint(0, 99) < Mine.RANDOM_MINE_CHANCE:
                    self.mine(choice(list(minable)))
                    return True

        return False

    def mine(self, point):
        self.actor.state.terrain_map.mine_point(point)
