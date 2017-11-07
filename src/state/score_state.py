from in_game_menu_state import InGameMenuState
from src.ui.ui import UI
import pygame
from src.constants import *
from src.ui.score_sheet import ScoreSheet


class ScoreState(InGameMenuState):

    def __init__(self, state_manager, game_state, back_drop, fade=True):

        InGameMenuState.__init__(self, state_manager, game_state, back_drop, fade=fade)
        self.score_sheet = ScoreSheet(game_state.score_keeper)

    def get_screen_image(self, back_drop, fade):

        surf = pygame.Surface((SCREENW, SCREENH)).convert()
        surf.blit(back_drop, (0, 0))
        if fade:
            surf.set_alpha(100)
        return surf

    def initialize_ui(self):
        return UI.create_score_ui(self)

    def handle_input(self):

        # returns true to exit game
        for event in pygame.event.get():

            if event.type == QUIT:
                self.trigger_exit()

            elif event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    self.return_to_main()

            elif event.type == KEYUP:

                pass

            elif event.type == MOUSEBUTTONDOWN:

                if event.button == 1:
                    self.ui.click(pygame.mouse.get_pos())

    def draw(self):
        self.score_sheet.draw(self.screen)
        self.ui.draw(self.screen)

    def return_to_main(self):
        self.set_next_state(self.state_manager.load_main_menu())
        self.trigger_exit()

    def retire_from_game(self):
        pass

    def return_to_game(self):
        pass

    def quit_program(self):
        self.set_next_state('exit')
        self.trigger_exit()
