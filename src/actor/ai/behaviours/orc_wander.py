from behaviour import Behaviour
from random import choice


class OrcWander(Behaviour):

    def __init__(self):

        Behaviour.__init__(self)

    def run_specifics(self):

        possible_moves = self.get_assault_adj()

        possible_moves.append(self.actor.coord)

        move = choice(possible_moves)
        self.actor.assault(move)
        self.ai_component.use_action()

    def get_assault_adj(self):

        adj = self.actor.state.terrain_map.get_passable_adj(self.actor.coord)

        blockers = self.actor.state.object_list.get_blockers()
        non_mushlock = filter(lambda x: x.key != 'mushlock', blockers)

        blocked_coords = set(map(lambda x: x.coord, non_mushlock))

        for point in adj[:]:

            if point in blocked_coords:
                adj.remove(point)
                continue

        return adj
