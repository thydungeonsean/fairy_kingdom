import pygame
from src.image.image_cache import ImageCache
from random import choice
from src.constants import *


class MapImage(object):

    PADDING = 8

    def __init__(self, map, state):

        self.state = state
        self.coord = (0, 0)
        self.map = map
        self.cache = ImageCache.get_instance()
        self.image = self.initialize_image()
    
    def draw(self, surface):
        surface.blit(self.image, self.coord)
    
    def set_coord(self, coord):
        self.coord = coord
        
    def initialize_image(self):
        
        cls = MapImage
        
        w = (self.map.w + cls.PADDING * 2) * TILEW
        h = (self.map.h + cls.PADDING * 2) * TILEH
        
        image = pygame.Surface((w, h)).convert()
        image.fill(SHROUD)
        
        return image
        
    def get_pixel_coord(self, (x, y)):
        cls = MapImage
        px = (x + cls.PADDING) * TILEW
        py = (y + cls.PADDING) * TILEH
        return px, py

    def reveal_tile(self, (x, y)):

        self.draw_tile((x, y))

    def draw_tile(self, (x, y)):

        terrain = self.map.get_tile((x, y))

        if self.tile_is_horizontal_wall((x, y)):
            image_key = choice((ImageCache.WALL_VARIANTS))
        else:
            image_key = terrain

        image = self.cache.get_image(image_key)
        image.set_coord(self.get_pixel_coord((x, y)))
        image.draw(self.image)

    def tile_is_horizontal_wall(self, (x, y)):

        return self.map.tile_is_horizontal_wall((x, y))
        
    def reveal_all(self):
        for y in range(self.map.h):
            for x in range(self.map.w):
                self.reveal_tile((x, y))

    def update(self, points):
        points = filter(lambda x: not self.state.shroud.point_is_hidden(x), points)
        for point in points:
            self.draw_tile(point)

    def make_rubble(self, (x, y)):

        image = self.cache.get_image(RUBBLE)
        image.set_coord(self.get_pixel_coord((x, y)))
        image.draw(self.image)

        if not self.state.shroud.point_is_hidden((x, y-1)) and self.state.terrain_map.get_tile((x, y-1)) == WALL:
            self.draw_tile((x, y-1))
