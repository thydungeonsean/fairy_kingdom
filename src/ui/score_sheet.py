from font_draw import FontDraw
from src.constants import *
import pygame


class ScoreSheet(object):

    w = SCALE * 200
    h = SCALE * 300
    label_box_w = 100*SCALE
    label_box_h = 30*SCALE
    score_box_w = 50*SCALE
    score_box_h = 30*SCALE

    layout = {0: 'MOST MUSHLOCKS',
              1: 'MOST HOUSES',
              2: 'FOOD COLLECTED',
              3: 'GEMS COLLECTED',
              4: 'TURNS SURVIVED',
              5: 'POWERS USED',
              6: 'ORCS SLAIN',
              9: 'TOTAL SCORE'}

    def __init__(self, score_keeper):

        self.score_keeper = score_keeper
        self.score_keeper.compute_score()

        self.score_dict = {
            'MOST MUSHLOCKS': str(self.score_keeper.most_mushlocks),
            'MOST HOUSES': str(self.score_keeper.most_mushhouses),
            'FOOD COLLECTED': str(self.score_keeper.food),
            'GEMS COLLECTED': str(self.score_keeper.gems),
            'TURNS SURVIVED': str(self.score_keeper.turns),
            'POWERS USED': str(self.score_keeper.powers_used),
            'ORCS SLAIN': str(self.score_keeper.orcs_slain),
            'TOTAL SCORE': str(self.score_keeper.score),
        }

        self.color = BLUE
        self.image = self.create_image()
        self.coord = (0, 0)

    def draw(self, surface):
        surface.blit(self.image, self.coord)

    def create_image(self):

        cls = ScoreSheet

        surface = pygame.Surface((cls.w, cls.h)).convert()

        for i in cls.layout.keys():

            key = cls.layout[i]

            text = key
            num = self.score_dict[key]

            label_image = FontDraw.get_instance().create_text_box(text, self.color, cls.label_box_w, cls.label_box_h)
            score_image = FontDraw.get_instance().create_text_box(num, self.color, cls.score_box_w, cls.score_box_h)

            label_coord = 0, i * cls.label_box_h
            score_coord = 150*SCALE, i * cls.label_box_h

            surface.blit(label_image, label_coord)
            surface.blit(score_image, score_coord)

        return surface
