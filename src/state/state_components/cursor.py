from src.constants import *
import pygame


class Cursor(object):

    POS = 1
    NEG = 0

    colors = {POS: (255, 255, 255), NEG: (255, 0, 0)}

    def __init__(self, state):

        self.state = state

        self.cursor = Cursor.POS
        self.coord = None
        self.pixel_coord = (0, 0)

        self.power = None

        self.shown = False

        self.images = self.set_images()

    def set_images(self):

        images = {
            Cursor.POS: self.get_cursor_image(Cursor.POS),
            Cursor.NEG: self.get_cursor_image(Cursor.NEG)
        }
        return images

    def get_cursor_image(self, code):
        surf = pygame.Surface((TILEW, TILEH)).convert()
        surf.fill(Cursor.colors[code])
        surf.set_alpha(100)
        return surf

    def get_coord(self):
        if self.shown:
            return self._get_coord()
        return None

    def _get_coord(self):
        mx, my = pygame.mouse.get_pos()
        relx = mx / TILEW
        rely = my / TILEH
        return relx, rely

    def update(self):
        new = self.get_coord()
        if new != self.coord and new is not None:
            self.change(new)
            coord_on_map = self.state.mouse_handler.get_mouse_coord()
            if self.state.terrain_map.point_in_bounds(coord_on_map) and self.power.point_is_valid(coord_on_map):
                self.cursor = Cursor.POS
            else:
                self.cursor = Cursor.NEG

    def change(self, (x, y)):

        self.coord = (x, y)
        self.pixel_coord = (x*TILEW, y*TILEH)

    def show(self):
        self.shown = True

    def hide(self):
        self.shown = False

    def draw(self, surface):
        if self.shown:
            surface.blit(self.images[self.cursor], self.pixel_coord)

    def bind_power(self, power):
        self.power = power
        self.show()

    def unbind_power(self):
        self.power = None
        self.hide()
