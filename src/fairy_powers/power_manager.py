from powers import *
from lure import Lure
from see import See
from sleep import Sleep
from gust import Gust
from river import River
from rock import Rock
from mark import Mark


class PowerManager(object):

    def __init__(self, state):

        self.state = state
        self.selected = None

        self.selection_dict = {
            LURE: False,
            SEE: False,
            SLEEP: False,
            GUST: False,
            RIVER: False,
            ROCK: False,
            MARK: False,
        }

    def select_power(self, power_key):
        pass

    @property
    def power_selected(self):
        return self.selected is not None

    def click_power_key(self, power_key):

        if self.selection_dict[power_key]:
            self.selection_dict[power_key] = False
            self.selected = None
            self.state.cursor.unbind_power()
        else:
            self.deselect_other_powers(power_key)
            self.selection_dict[power_key] = True
            self.selected = self.load_selected(power_key)
            self.selected.load_state(self.state)
            self.state.cursor.bind_power(self.selected)

        # any updating of the panels now
        self.update_buttons()

    def click_lure(self):
        self.click_power_key(LURE)

    def click_see(self):
        self.click_power_key(SEE)

    def click_sleep(self):
        self.click_power_key(SLEEP)

    def click_gust(self):
        self.click_power_key(GUST)

    def click_river(self):
        self.click_power_key(RIVER)

    def click_rock(self):
        self.click_power_key(ROCK)

    def click_mark(self):
        self.click_power_key(MARK)

    def deselect_other_powers(self, power_key):
        for k in filter(lambda x: x != power_key, self.selection_dict.keys()):
            self.selection_dict[k] = False

    def load_selected(self, power_key):
        if power_key == LURE:
            return Lure.get_instance()
        elif power_key == SEE:
            return See.get_instance()
        elif power_key == SLEEP:
            return Sleep.get_instance()
        elif power_key == GUST:
            return Gust.get_instance()
        elif power_key == RIVER:
            return River.get_instance()
        elif power_key == ROCK:
            return Rock.get_instance()
        elif power_key == MARK:
            return Mark.get_instance()
        # .......
        raise Exception('invalid power key')

    def update_buttons(self):

        for button in self.state.ui.elements:

            if button.text not in POWER_BUTTONS:
                continue

            key = name_to_key[button.text]
            if self.selection_dict[key]:  # button is selected
                button.highlight()
            elif not self.selection_dict[key]:
                button.normal()

