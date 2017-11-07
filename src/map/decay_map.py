from src.constants import *


class DecayMap(object):

    DECAY_TIME = 10

    DECAYABLE = STUMP_L, STUMP_R, STUMP

    def __init__(self, state):
        self.state = state
        self.decay_map = {}

    def run(self):

        complete = []
        for k, v in self.decay_map.iteritems():
            self.decay_map[k] += 1
            if self.decay_map[k] >= DecayMap.DECAY_TIME:
                complete.append(k)

        for point in complete:
            self.degrade_point(point)

        if complete:
            self.state.path_finding_map.compute()

    def degrade_point(self, point):

        if self.state.terrain_map.get_tile(point) in DecayMap.DECAYABLE:
            # TODO, have progression of decay for certain objects
            self.state.terrain_map.set_tile(point, FLOOR)
            self.state.map_image.update([point])
            del self.decay_map[point]

    def add_decayable(self, point):
        self.decay_map[point] = 1
