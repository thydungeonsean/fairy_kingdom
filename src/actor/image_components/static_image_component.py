from image_component import ImageComponent
from src.image.image_cache import ImageCache


class StaticImageComponent(ImageComponent):

    def __init__(self, owner, key):
        ImageComponent.__init__(self, owner, key)

    def initialize_images(self):
        return ImageCache.get_instance().get_image(self.key)
