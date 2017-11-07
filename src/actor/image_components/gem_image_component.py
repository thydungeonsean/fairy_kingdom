from image_component import ImageComponent
from src.image.image import Image


class GemImageComponent(ImageComponent):

    HIDDEN = 0
    REVEALED = 1
    VISIBLE = 2

    def __init__(self, owner):

        ImageComponent.__init__(self, owner, 'gem', transparent=True)
        self.visible_state = GemImageComponent.HIDDEN
        cls = GemImageComponent
        self.draw_for_state = {cls.HIDDEN: self.draw_hidden, cls.REVEALED: self.draw_revealed,
                               cls.VISIBLE: self.draw_revealed}
        self.position_for_state = {cls.HIDDEN: self.pos_hidden, cls.REVEALED: self.pos_revealed,
                                   cls.VISIBLE: self.pos_revealed}

    def initialize_images(self):
        cls = GemImageComponent
        return {cls.REVEALED: Image('buried_gem', transparent=True),
                cls.VISIBLE: Image('gem', transparent=True)}

    @property
    def current_image(self):
        return self.images[self.visible_state]

    def set_position(self):
        self.position_for_state[self.visible_state]()

    def draw(self, surface):

        self.draw_for_state[self.visible_state](surface)

    def draw_hidden(self, surface):
        pass

    def draw_revealed(self, surface):
        self.current_image.draw(surface)

    def pos_hidden(self):
        pass

    def pos_revealed(self):
        self.current_image.set_coord(self.get_relative_coord())

    def change_visibility(self, new):
        self.visible_state = new
