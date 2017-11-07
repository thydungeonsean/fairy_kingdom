from state_template import *


class InGameMenuUI(StateTemplate):

    x = (SCREENW - Button.BUTTON_W) / 2
    y = (SCREENH - Button.BUTTON_H) / 2
    return_button_coord = x, y
    retire_button_coord = x, y + Button.BUTTON_H + SCALE*5
    quit_button_coord = x, y + Button.BUTTON_H*2 + SCALE*5*2

    def __init__(self, state, ui):

        StateTemplate.__init__(self, state, ui)

    def initialize_elements(self):

        return_button = self.make_return_button()
        retire_button = self.make_retire_button()
        quit_button = self.make_quit_button()

        return [return_button, retire_button, quit_button]

    def make_return_button(self):

        return self.make_button(InGameMenuUI.return_button_coord, 'RETURN', self.state.return_to_game)

    def make_retire_button(self):

        return self.make_button(InGameMenuUI.retire_button_coord, 'RETIRE', self.state.retire_from_game)

    def make_quit_button(self):

        return self.make_button(InGameMenuUI.quit_button_coord, 'QUIT', self.state.quit_program)
