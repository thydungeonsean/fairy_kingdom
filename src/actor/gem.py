from map_object import MapObject
from image_components.gem_image_component import GemImageComponent


class Gem(MapObject):

    HIDDEN = 0
    REVEALED = 1
    VISIBLE = 2

    def __init__(self, state, coord):

        MapObject.__init__(self, state, 'gem', coord)
        self.visible = Gem.HIDDEN
        self.flag = MapObject.OBJECT
        self.blocks = False

        self.initialize_visible()

    def set_image_component(self):
        return GemImageComponent(self)

    def initialize_visible(self):

        if self.state.terrain_map.point_is_minable(self.coord):
            visible = Gem.HIDDEN
        else:
            visible = Gem.VISIBLE

        self.set_visible(visible)

    def set_visible(self, new):
        self.visible = new
        self.image_component.change_visibility(self.visible)

    def reveal_gem(self):
        self.set_visible(Gem.REVEALED)

    def discover_gem(self):
        self.set_visible(Gem.VISIBLE)

    def uncover_gem(self):
        self.set_visible(Gem.VISIBLE)

    @property
    def hidden(self):
        return self.visible == Gem.HIDDEN

    def on_mushlock(self, mush):
        if mush.pick_up_gem():
            self.die()
