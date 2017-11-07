from state_template import *


class GameStateUI(StateTemplate):

    number_of_buttons = 7
    buffer = SCALE * 5
    buffed_button_h = buffer + Button.BUTTON_H

    x = SCREENW - Button.BUTTON_W - buffer
    y = (SCREENH - (Button.BUTTON_H * number_of_buttons) - (buffer * (number_of_buttons-1))) / 4

    # lure
    lure_coord = x, y
    lure_text = 'LURE'
    # see
    see_coord = x, y + (buffed_button_h * 1)
    see_text = 'SEE'
    # sleep
    sleep_coord = x, y + (buffed_button_h * 2)
    sleep_text = 'SLEEP'
    # gust
    gust_coord = x, y + (buffed_button_h * 3)
    gust_text = 'GUST'
    # river
    river_coord = x, y + (buffed_button_h * 4)
    river_text = 'RIVER'
    # rock
    rock_coord = x, y + (buffed_button_h * 5)
    rock_text = 'ROCK'
    # mark
    mark_coord = x, y + (buffed_button_h * 6)
    mark_text = 'MARK'

    # end turn
    end_turn_coord = x, SCREENH - Button.BUTTON_H - buffer
    end_turn_text = 'END TURN'

    # in game menu
    menu_coord = x, buffer
    menu_text = 'MENU'

    def __init__(self, state, ui):

        StateTemplate.__init__(self, state, ui)

    def initialize_elements(self):

        menu_button = self.make_menu_button()

        lure_button = self.make_lure_button()
        see_button = self.make_see_button()
        sleep_button = self.make_sleep_button()
        gust_button = self.make_gust_button()
        river_button = self.make_river_button()
        rock_button = self.make_rock_button()
        mark_button = self.make_mark_button()

        end_turn_button = self.make_end_turn_button()

        return [menu_button, lure_button, see_button, sleep_button, gust_button, river_button, rock_button, mark_button,
                end_turn_button]

    def make_menu_button(self):
        cls = GameStateUI
        return self.make_button(cls.menu_coord, cls.menu_text, self.state.open_in_game_menu)

    def make_lure_button(self):
        cls = GameStateUI
        return self.make_button(cls.lure_coord, cls.lure_text, self.state.power_manager.click_lure)

    def make_see_button(self):
        cls = GameStateUI
        return self.make_button(cls.see_coord, cls.see_text, self.state.power_manager.click_see)

    def make_sleep_button(self):
        cls = GameStateUI
        return self.make_button(cls.sleep_coord, cls.sleep_text, self.state.power_manager.click_sleep)

    def make_gust_button(self):
        cls = GameStateUI
        return self.make_button(cls.gust_coord, cls.gust_text, self.state.power_manager.click_gust)

    def make_river_button(self):
        cls = GameStateUI
        return self.make_button(cls.river_coord, cls.river_text, self.state.power_manager.click_river)

    def make_rock_button(self):
        cls = GameStateUI
        return self.make_button(cls.rock_coord, cls.rock_text, self.state.power_manager.click_rock)

    def make_mark_button(self):
        cls = GameStateUI
        return self.make_button(cls.mark_coord, cls.mark_text, self.state.power_manager.click_mark)

    def make_end_turn_button(self):
        cls = GameStateUI
        return self.make_button(cls.end_turn_coord, cls.end_turn_text, self.state.end_player_turn)
