from src.constants import *
import pygame


class AbstractState(object):

    def __init__(self, state_manager):

        self.state_manager = state_manager

        self.exit_state = False
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.get_surface()

        self.next_state = 'exit'
        self.fullscreen = False

        self.ui = self.initialize_ui()

    def initialize_ui(self):
        raise NotImplementedError

    def handle_input(self):

        # returns true to exit game
        for event in pygame.event.get():

            if event.type == QUIT:
                self.trigger_exit()

            elif event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    pass

            elif event.type == KEYUP:

                pass

            elif event.type == MOUSEBUTTONDOWN:

                if event.button == 1:
                    self.ui.click(pygame.mouse.get_pos())

    def trigger_exit(self):
        self.exit_state = True

    def run(self):
        pass

    def draw(self):
        raise NotImplementedError

    def main(self):

        while True:

            if self.exit_state:
                return True

            self.handle_input()

            self.run()

            self.draw()
            pygame.display.update()

            self.clock.tick(FPS)

    def get_next_state(self):
        return self.next_state

    def set_next_state(self, next_state):
        self.next_state = next_state

    def reset_state(self):
        self.set_next_state('exit')
        self.exit_state = False

    def toggle_fullscreen(self):
        if self.fullscreen:
            self.fullscreen = False
            pygame.display.set_mode((SCREENW, SCREENH))
        else:
            self.fullscreen = True
            pygame.display.set_mode((SCREENW, SCREENH), FULLSCREEN)
