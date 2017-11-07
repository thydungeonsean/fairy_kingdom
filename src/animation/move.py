from animation import *


class Move(Animation):

    X_AXIS = 0
    Y_AXIS = 1

    dist = {X_AXIS: TILEW, Y_AXIS: TILEH}

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

        axis, mod = Move.direction_build[self.direction]

        mod_sequence = self.lerp_mods(mod, axis)
        return self.compile_modifier_sequence(mod_sequence, axis)

    def lerp_mods(self, base_mod, axis):

        final = base_mod * Move.dist[axis]

        mods = []

        for i in range(AI_SPEED, 0, -1):

            percent_done = i / float(AI_SPEED)
            mods.append(int(percent_done * final))

        return mods

    def compile_modifier_sequence(self, mod_sequence, axis):

        seq = {}

        for i in range(len(mod_sequence)):

            mod = [0, 0]
            mod[axis] = mod_sequence[i]

            seq[i] = tuple(mod)

        return seq