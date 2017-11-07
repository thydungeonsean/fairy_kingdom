from animated_image_component import AnimatedImageComponent
from src.image.image import Image
from src.constants import *


class MushlockImageComponent(AnimatedImageComponent):

    on_head = (0, -TILEH / 2)
    in_hand = (0, 0)

    carry_point_dict = {
        'food': on_head,
        'carried_gem': on_head,
        'empty_bucket': on_head,
        'full_bucket': on_head,

        'zzz_a': on_head,
        'zzz_b': on_head,

        'carried_spear': in_hand,
        'carried_pick': in_hand,
    }

    def __init__(self, owner):

        AnimatedImageComponent.__init__(self, owner, 'mushlock', transparent=True)
        self.carried_image = None
        self.sleeping = False
        self.sleep_images = self.set_sleep_images()

    @property
    def current_image(self):
        if not self.sleeping:
            return self.images[self.ani_key]
        else:
            return self.images['c']

    @property
    def sleep_image(self):
        return self.sleep_images[self.ani_key]

    def initialize_images(self):
        images = {}
        self.add_frame(images, 'a')
        self.add_frame(images, 'b')
        self.add_frame(images, 'c')
        return images

    def set_sleep_images(self):
        images = {
                  'a': Image('zzz_a', transparent=True),
                  'b': Image('zzz_b', transparent=True)
                  }
        return images

    def update_carried(self):
        if self.owner.carrying:
            self.carried_image = self.load_carried_image(self.owner.carried)
        else:
            self.carried_image = None

    def set_position(self):
        self.current_image.set_coord(self.get_relative_coord())
        if self.carried_image is not None:
            c = self.get_carried_item_coord(self.owner.carried)
            self.carried_image.set_coord(c)
        elif self.sleeping:
            c = self.get_sleep_coord()
            self.sleep_image.set_coord(c)

    def draw(self, surface):
        self.current_image.draw(surface)
        if self.carried_image is not None:
            self.carried_image.draw(surface)
        elif self.sleeping:
            self.sleep_image.draw(surface)

    def get_carried_item_coord(self, item):
        x, y = self.current_image.coord
        modx, mody = MushlockImageComponent.carry_point_dict[item]
        x += modx
        y += mody
        if self.ani_key == 'b':
            y += SCALE
        return x, y

    def load_carried_image(self, obj):
        return Image(obj, transparent=True)

    def update_sleep(self):
        self.sleeping = self.owner.sleeping

    def get_sleep_coord(self):

        x, y = self.current_image.coord
        modx, mody = MushlockImageComponent.on_head
        return x+modx, y+mody