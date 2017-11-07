from map_object import MapObject
from src.constants import *
from image_components.static_image_component import StaticImageComponent


class Plant(MapObject):

    def __init__(self, state, coord):

        MapObject.__init__(self, state, PLANT, coord)
        self.blocks = False

    def set_image_component(self):
        return StaticImageComponent(self, self.key)

    def on_mushlock(self, mush):
        if mush.pick_up_food():
            self.die()
