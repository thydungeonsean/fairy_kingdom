from animation import Animation
from src.constants import *


class Bump(Animation):

    X_AXIS = 0
    Y_AXIS = 1

    seq = (1, 2, 4, 2, 1)

    direction_build = {
        'up': (Y_AXIS, 1),
        'down': (Y_AXIS, -1),
        'right': (X_AXIS, -1),
        'left': (X_AXIS, 1),
    }

    def __init__(self, direction):
        self.direction = direction
        Animation.__init__(self)

    def generate_modifier_sequence(self):

        axis, mod = Bump.direction_build[self.direction]

        mod_sequence = Bump.seq
        return self.compile_modifier_sequence(mod_sequence, axis)

    def compile_modifier_sequence(self, mod_sequence, axis):

        seq = {}

        for i in range(len(mod_sequence)):

            mod = [0, 0]
            mod[axis] = mod_sequence[i] * SCALE

            seq[i] = tuple(mod)

        remainder = AI_SPEED - len(mod_sequence)
        for i in range(remainder):
            seq[i + remainder] = (0, 0)

        return seq