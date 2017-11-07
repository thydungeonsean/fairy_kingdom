from abstract_state import *
from src.ui.font_draw import FontDraw
import pygame
from src.constants import *


class OpeningState(AbstractState):

    def __init__(self, state_manager):

        AbstractState.__init__(self, state_manager)
        self.draw_opening_screen()

    def initialize_ui(self):
        return None

    def handle_input(self):

        # returns true to exit game
        for event in pygame.event.get():

            if event.type == QUIT:
                self.trigger_exit()

            elif event.type == KEYDOWN:

                self.return_to_main()

            elif event.type == KEYUP:

                pass

            elif event.type == MOUSEBUTTONDOWN:

                self.return_to_main()

    def draw(self):
        pass

    def return_to_main(self):
        self.set_next_state(self.state_manager.load_main_menu())
        self.trigger_exit()

    def draw_opening_screen(self):

        self.screen.fill(BLACK)
        w = SCALE*100
        h = SCALE*50
        title = FontDraw.get_instance().create_text_box('FAIRY KINGDOM', BLUE, w, h)

        tw = w*3
        th = h*3
        title = pygame.transform.scale(title, (tw, th))



        title_coord = ((SCREENW - tw) / 2, (SCREENH - th) / 2)

        self.screen.blit(title, title_coord)
