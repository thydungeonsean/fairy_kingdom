import pygame
from src.constants import *
from tile_key import tiles, load_tile_sheet, tile_rect


class Image(object):
    
    def __init__(self, key, transparent=False):

        self.surface = self.initialize_surface(key, transparent)
        self.coord = (0, 0)
        
    def initialize_surface(self, key, transparent):

        surface = pygame.Surface((BASE_TILE_W, BASE_TILE_H)).convert()
        surface.fill(BLACK)

        x_offset, y_offset = tiles[key]
        tile_rect.topleft = x_offset*BASE_TILE_W, y_offset*BASE_TILE_H
        surface.blit(load_tile_sheet(), (0, 0), tile_rect)

        surface = pygame.transform.scale(surface, (TILEW, TILEH)).convert()

        if transparent:
            surface.set_colorkey(COLORKEY)

        return surface
        
    def set_coord(self, coord):
        self.coord = coord
        
    def draw(self, surface):
        surface.blit(self.surface, self.coord)
        
    def run(self):
        pass
