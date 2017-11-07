from src.ui.button import Button
from src.constants import *


class StateTemplate(object):

    def __init__(self, state, ui):

        self.state = state
        self.ui = ui
        self.elements = self.initialize_elements()

    def add_to_state(self):
        for element in self.elements:
            self.ui.add_element(element)

    def initialize_elements(self):
        raise NotImplementedError

    def make_button(self, coord, text, func):
        button = Button(coord, text)
        button.on_click = func
        return button
