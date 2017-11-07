from state_templates.game_state_ui import GameStateUI
from state_templates.main_menu_ui_template import MainMenuUI
from state_templates.in_game_menu_ui import InGameMenuUI
from state_templates.score_state_ui import ScoreStateUI


class UI(object):

    @classmethod
    def create_game_ui(cls, state):

        ui = cls(state)

        GameStateUI(state, ui).add_to_state()

        return ui

    @classmethod
    def create_main_menu_ui(cls, state):

        ui = cls(state)

        MainMenuUI(state, ui).add_to_state()

        return ui

    @classmethod
    def create_score_ui(cls, state):

        ui = cls(state)

        ScoreStateUI(state, ui).add_to_state()

        return ui

    @classmethod
    def create_in_game_menu_ui(cls, state):

        ui = cls(state)

        InGameMenuUI(state, ui).add_to_state()

        return ui

    def __init__(self, state):

        self.state = state
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)
        element.set_ui(self)

    def remove_element(self, element):
        self.elements.remove(element)

    def click(self, point):
        for element in self.elements:
            clicked = element.click(point)
            if clicked:
                return True
        return False

    def run(self):
        for element in self.elements:
            element.run()

    def draw(self, surface):
        for element in self.elements:
            element.draw(surface)
