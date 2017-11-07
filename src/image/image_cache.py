from src.constants import *
from image import Image
import pygame


class ImageCache(object):

    instance = None
    
    WALL_VARIANTS = HOR_WALL_1, HOR_WALL_2, HOR_WALL_3
    
    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance
        
    def __init__(self):
    
        self.cache = {}
        
    def get_image(self, key):
    
        if self.cache.get(key, None) is None:
            self.load_image(key)
        return self.cache.get(key)
        
    def load_image(self, key):
        
        image = Image(key)
        self.cache[key] = image
