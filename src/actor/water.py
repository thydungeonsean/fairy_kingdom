from map_object import MapObject
from src.actor.image_components.animated_image_component import AnimatedImageComponent


class Water(MapObject):

    def __init__(self, state, river, coord):
        MapObject.__init__(self, state, 'water', coord)
        self.river = river
        self.blocks = False

    def set_image_component(self):
        return AnimatedImageComponent(self, self.key, static=True)

    def on_mushlock(self, mush):
        mush.difficult_terrain()

