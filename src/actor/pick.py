from map_object import MapObject
from image_components.image_component import ImageComponent


class Pick(MapObject):

    def __init__(self, state, point):

        MapObject.__init__(self, state, 'pick', point)
        self.flag = MapObject.OBJECT
        self.blocks = False

    def on_mushlock(self, mush):
        if mush.pick_up_pick():
            self.die()

    def set_image_component(self):
        return ImageComponent(self, 'pick', transparent=True)