from src.actor.image_components.image_component import ImageComponent


class MapObject(object):

    OBJECT = 0
    ACTOR = 1

    def __init__(self, state, key, coord):

        self.flag = MapObject.OBJECT
        self.state = state
        self.key = key
        self.blocks = False

        self.coord = coord
        self.image_component = self.set_image_component()

        self.ai_component = None
        self.animation = None

    def set_image_component(self):
        return ImageComponent(self, self.key)

    def draw(self, surface):
        self.image_component.set_position()
        self.image_component.draw(surface)

    def run(self):

        self.image_component.run()

    def move(self, new):
        self.coord = new

    def bump(self):
        pass

    def die(self):
        self.state.object_list.remove_object(self)

    def on_mushlock(self, mush):
        pass
