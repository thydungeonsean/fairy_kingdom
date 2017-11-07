import pygame
from src.constants import *


class MouseHandler(object):

    def __init__(self, state):

        self.state = state

    def left_click(self):

        ui_clicked = self.click_ui()
        if not ui_clicked and self.state.power_manager.power_selected and not self.state.effect_handler.effects:
            self.try_to_cast_power()

    def get_mouse_coord(self):
        mx, my = pygame.mouse.get_pos()
        relx = mx / TILEW
        rely = my / TILEH
        relx += self.state.view.coord[0]
        rely += self.state.view.coord[1]
        return relx, rely

    def click_ui(self):

        pos = pygame.mouse.get_pos()
        return self.state.ui.click(pos)

    @property
    def selected_power(self):
        return self.state.power_manager.selected

    def try_to_cast_power(self):
        coord = self.get_mouse_coord()
        if self.state.terrain_map.point_in_bounds(coord) and self.selected_power.point_is_valid(coord):

            self.selected_power.use_power(coord)
            self.state.score_keeper.add_power_use()
            if self.state.ONE_POWER_PER_TURN_MODE:
                self.state.flag_end_turn()
