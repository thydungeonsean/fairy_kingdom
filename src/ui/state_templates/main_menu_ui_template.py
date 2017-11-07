from state_template import *


class MainMenuUI(StateTemplate):

    x = (SCREENW - Button.BUTTON_W) / 2
    y = (SCREENH - Button.BUTTON_H) / 2
    start_button_coord = x, y
    quit_button_coord = x, y + Button.BUTTON_H + SCALE*5

    def __init__(self, state, ui):

        StateTemplate.__init__(self, state, ui)

    def initialize_elements(self):

        start_button = self.make_start_button()
        quit_button = self.make_quit_button()

        return [start_button, quit_button]

    def make_start_button(self):

        return self.make_button(MainMenuUI.start_button_coord, 'NEW GAME', self.state.start_new_game)

    def make_quit_button(self):

        return self.make_button(MainMenuUI.quit_button_coord, 'QUIT', self.state.quit_game)
