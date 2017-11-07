from map_object import MapObject
from src.animation.animation_archive import AnimationArchive
from src.constants import AI_SPEED


class Actor(MapObject):

    relative_move = {
        (0, 1): AnimationArchive.MOVE_DOWN,
        (0, -1): AnimationArchive.MOVE_UP,
        (1, 0): AnimationArchive.MOVE_RIGHT,
        (-1, 0): AnimationArchive.MOVE_LEFT,
        (0, 0): None,
    }

    relative_bump = {
        (0, 1): AnimationArchive.BUMP_DOWN,
        (0, -1): AnimationArchive.BUMP_UP,
        (1, 0): AnimationArchive.BUMP_RIGHT,
        (-1, 0): AnimationArchive.BUMP_LEFT,
        (0, 0): None,
    }

    def __init__(self, state, key, coord):
        MapObject.__init__(self, state, key, coord)

        self.animation = None
        self.animation_step = 0

    def move(self, new):
        self.animation = self.set_move_animation(new)
        self.coord = new

    def run(self):
        if self.animation is not None:
            self.step_animation()
        self.image_component.run()

    def step_animation(self):
        self.animation_step += 1
        if self.animation_step >= AI_SPEED:
            self.animation = None
            self.animation_step = 0

    def set_move_animation(self, (nx, ny)):
        x, y = self.coord
        diff = nx - x, ny - y
        if diff == (0, 0):
            return None
        code = Actor.relative_move[diff]
        return AnimationArchive.move[code]

    def set_bump_animation(self, (nx, ny)):
        x, y = self.coord
        diff = nx - x, ny - y
        if diff == (0, 0):
            return None
        code = Actor.relative_bump[diff]
        return AnimationArchive.bump[code]
