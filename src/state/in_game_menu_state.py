from abstract_state import AbstractState
from src.ui.ui import UI
import pygame
from src.constants import *


class InGameMenuState(AbstractState):

    def __init__(self, state_manager, game_state, back_drop, fade=True):

        AbstractState.__init__(self, state_manager)
        self.game_state = game_state
        self.back_drop = self.get_screen_image(back_drop, fade)

        self.first_frame = True

    def init_screen(self):

        self.screen.fill(BLACK)
        self.screen.blit(self.back_drop, (0, 0))

    def get_screen_image(self, back_drop, fade):

        surf = pygame.Surface((SCREENW, SCREENH)).convert()
        surf.blit(back_drop, (0, 0))
        surf.set_alpha(100)
        return surf

    def handle_input(self):

        # returns true to exit game
        for event in pygame.event.get():

            if event.type == QUIT:
                self.trigger_exit()

            elif event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    self.return_to_game()

            elif event.type == KEYUP:

                pass

            elif event.type == MOUSEBUTTONDOWN:

                if event.button == 1:
                    self.ui.click(pygame.mouse.get_pos())

    def initialize_ui(self):
        return UI.create_in_game_menu_ui(self)

    def draw(self):

        self.ui.draw(self.screen)

    def retire_from_game(self):
        next_state = self.state_manager.load_score_state(self.game_state, self.back_drop, fade=False)
        self.set_next_state(next_state)
        self.trigger_exit()

    def return_to_game(self):
        self.set_next_state(self.game_state)
        self.game_state.reset_state()
        self.trigger_exit()

    def quit_program(self):
        self.set_next_state('exit')
        self.trigger_exit()

    def run(self):
        if self.first_frame:
            self.first_frame = False
            self.init_screen()

