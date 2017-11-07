from map_object import MapObject
from src.actor.image_components.animated_image_component import AnimatedImageComponent


class Lure(MapObject):

    def __init__(self, state, coord):

        MapObject.__init__(self, state, 'lure', coord)
        self.blocks = False
        self.flag = MapObject.ACTOR

    def set_image_component(self):
        return AnimatedImageComponent(self, self.key, transparent=True)

    def on_mushlock(self, mush):
        self.die()
        self.state.path_finding_map.compute_lure_map()
