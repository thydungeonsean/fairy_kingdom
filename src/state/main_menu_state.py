from abstract_state import AbstractState
from src.ui.ui import UI
from src.constants import BLACK


class MainMenuState(AbstractState):

    def __init__(self, state_manager):

        AbstractState.__init__(self, state_manager)
        self.first_frame = True

    def init_screen(self):

        self.screen.fill(BLACK)

    def initialize_ui(self):
        return UI.create_main_menu_ui(self)

    def draw(self):
        self.ui.draw(self.screen)

    def start_new_game(self):
        self.set_next_state(self.state_manager.load_new_game())
        self.trigger_exit()

    def quit_game(self):
        self.set_next_state('exit')
        self.trigger_exit()

    def run(self):
        if self.first_frame:
            self.first_frame = False
            self.init_screen()
