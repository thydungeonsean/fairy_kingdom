from src.actor.image_components.image_component import ImageComponent, Image
from src.image.image_cache import ImageCache


class AnimatedImageComponent(ImageComponent):

    ANI_SPEED = 15

    def __init__(self, owner, key, transparent=False, static=False):

        self.static = static
        ImageComponent.__init__(self, owner, key, transparent=transparent)

        self.images = self.initialize_images()
        self.ani_key = 'a'
        self.tick = 0

    def initialize_images(self):
        images = {}
        self.add_frame(images, 'a')
        self.add_frame(images, 'b')
        return images

    def add_frame(self, images, ani_key):
        if self.static:
            self.add_static_image_ref(images, ani_key)
        else:
            images[ani_key] = Image('_'.join((self.key, ani_key)), transparent=self.transparent)

    def add_static_image_ref(self, images, ani_key):

        image_key = '_'.join((self.key, ani_key))
        images[ani_key] = ImageCache.get_instance().get_image(image_key)

    @property
    def current_image(self):
        return self.images[self.ani_key]

    def run(self):
        self.tick += 1
        if self.tick >= AnimatedImageComponent.ANI_SPEED:
            self.tick = 0
            self.switch_image()

    def switch_image(self):
        if self.ani_key == 'a':
            self.ani_key = 'b'
        else:
            self.ani_key = 'a'
