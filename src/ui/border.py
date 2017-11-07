import pygame


class Border(object):

    def __init__(self, owner, color):

        self.color = color
        self.owner = owner
        self.rect = self.owner.surface.get_rect()

    def draw(self, surface):

        pygame.draw.rect(surface, self.color, self.rect, 2)

    def change_color(self, new_color):
        self.color = new_color
