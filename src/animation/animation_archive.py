from move import Move
from bump import Bump


class AnimationArchive(object):

    MOVE_UP = 0
    MOVE_RIGHT = 1
    MOVE_DOWN = 2
    MOVE_LEFT = 3

    BUMP_UP = 4
    BUMP_RIGHT = 5
    BUMP_DOWN = 6
    BUMP_LEFT = 7

    move = {
        MOVE_UP: Move('up'),
        MOVE_RIGHT: Move('right'),
        MOVE_DOWN: Move('down'),
        MOVE_LEFT: Move('left'),
    }

    bump = {
        BUMP_UP: Bump('up'),
        BUMP_RIGHT: Bump('right'),
        BUMP_DOWN: Bump('down'),
        BUMP_LEFT: Bump('left'),
    }
