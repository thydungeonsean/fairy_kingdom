from src.constants import *


class Animation(object):

    def __init__(self):

        self.modifier_sequence = self.generate_modifier_sequence()

    def generate_modifier_sequence(self):
        raise NotImplementedError

    def get_modifiers(self, frame):
        return self.modifier_sequence[frame]
