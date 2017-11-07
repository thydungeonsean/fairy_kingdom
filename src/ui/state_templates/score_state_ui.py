from state_template import StateTemplate, Button
from src.constants import *


class ScoreStateUI(StateTemplate):

    x = SCALE*5
    y = (SCREENH - Button.BUTTON_H) - SCALE*5
    return_button_coord = x, y

    def __init__(self, state, ui):

        StateTemplate.__init__(self, state, ui)

    def initialize_elements(self):

        return_button = self.make_return_button()

        return [return_button]

    def make_return_button(self):

        return self.make_button(ScoreStateUI.return_button_coord, 'MAIN MENU', self.state.return_to_main)
