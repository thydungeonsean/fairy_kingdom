import pygame
from src.constants import *


class FontDraw(object):

    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        self.font = pygame.font.Font('assets/oryxtype.ttf', 16)

    def create_text_image(self, text, color):

        font_image = self.font.render(text, False, color)
        w = font_image.get_width() * SCALE
        h = font_image.get_height() * SCALE

        font_image = pygame.transform.scale(font_image, (w, h))

        return font_image

    def create_text_box(self, text, color, w, h):

        text_image = self.create_text_image(text, color)

        tw = text_image.get_width()
        th = text_image.get_height()

        text_x = (w - tw) / 2
        text_y = (h - th) / 2 - (SCALE*2)

        final_image = pygame.Surface((w, h)).convert()
        final_image.fill(BLACK)
        final_image.blit(text_image, (text_x, text_y))

        return final_image
