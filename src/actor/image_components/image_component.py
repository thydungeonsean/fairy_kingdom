from src.image.image import Image
from src.constants import *


class ImageComponent(object):

    def __init__(self, owner, key, transparent=False):

        self.owner = owner
        self.key = key
        self.transparent = transparent

        self.images = self.initialize_images()

    def initialize_images(self):
        return Image(self.key, transparent=self.transparent)

    @property
    def current_image(self):
        return self.images

    def set_position(self):
        self.current_image.set_coord(self.get_relative_coord())

    def run(self):
        pass

    def draw(self, surface):
        self.current_image.draw(surface)

    def get_relative_coord(self):

        ax, ay = self.owner.coord
        vx, vy = self.owner.state.view.coord

        if self.owner.animation is not None:
            ani_x, ani_y = self.owner.animation.get_modifiers(self.owner.animation_step)
        else:
            ani_x = 0
            ani_y = 0

        return (ax - vx) * TILEW + ani_x, (ay - vy) * TILEH + ani_y
