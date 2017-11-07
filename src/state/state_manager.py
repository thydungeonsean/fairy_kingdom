from main_menu_state import MainMenuState
from opening_state import OpeningState
from in_game_menu_state import InGameMenuState
from game_state import GameState
from score_state import ScoreState


class StateManager(object):

    def __init__(self):

        self.current_state = OpeningState(self)

    def main(self):

        while self.current_state is not None:
            complete = self.current_state.main()
            if complete:
                next_state_key = self.current_state.get_next_state()
                self.current_state = self.load_next_state(next_state_key)

    def load_next_state(self, next_state):
        if next_state == 'exit':
            return None
        else:
            return next_state

    def load_main_menu(self):
        state = MainMenuState(self)
        return state

    def load_new_game(self):
        state = GameState(self)
        return state

    def load_in_game_menu(self, game_state, back_drop):
        state = InGameMenuState(self, game_state, back_drop)
        return state

    def load_score_state(self, game_state, back_drop, fade):
        state = ScoreState(self, game_state, back_drop, fade=fade)
        return state
