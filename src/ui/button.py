import pygame
from src.constants import *
from border import Border
from font_draw import FontDraw


class Button(object):

    BUTTON_W = SCALE * 100
    BUTTON_H = SCALE * 20

    START_COLOR = BLUE
    HIGHLIGHT_COLOR = YELLOW

    def __init__(self, coord, text):

        self.coord = coord
        self.w = Button.BUTTON_W
        self.h = Button.BUTTON_H

        self.ui = None

        self.color = Button.START_COLOR

        self.surface = self.initialize_surface()
        self.border = Border(self, self.color)
        self.text = text

        self.render_image()

    def initialize_surface(self):

        image = pygame.Surface((self.w, self.h)).convert()
        image.fill(BLACK)

        return image

    def set_ui(self, ui):
        self.ui = ui

    @property
    def x(self):
        return self.coord[0]

    @property
    def y(self):
        return self.coord[1]

    def point_is_over(self, (x, y)):
        return self.x <= x < self.x + self.w and self.y <= y < self.y + self.h

    def click(self, point):
        if self.point_is_over(point):
            self.on_click()
            return True
        return False

    def on_click(self):
        pass
        print self.text

    def render_image(self):
        text_image = FontDraw.get_instance().create_text_box(self.text, self.color, self.w, self.h)
        self.surface.blit(text_image, (0, 0))
        self.border.draw(self.surface)

    def draw(self, surface):

        surface.blit(self.surface, self.coord)

    def run(self):
        pass

    def update_button(self):
        self.render_image()

    def highlight(self):
        self.color = Button.HIGHLIGHT_COLOR
        self.border.change_color(self.color)
        self.update_button()

    def normal(self):
        self.color = Button.START_COLOR
        self.border.change_color(self.color)
        self.update_button()

