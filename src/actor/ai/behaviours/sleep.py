from behaviour import Behaviour
from random import randint


class Sleep(Behaviour):

    MIN = 10
    MAX = 20

    SLEEP_COST = 5

    def __init__(self):

        Behaviour.__init__(self)

    def run_specifics(self):
        self.rest()

    def rest(self):
        self.actor.fall_asleep()
        self.ai_component.fatigue -= randint(Sleep.MIN, Sleep.MAX)
        self.ai_component.use_action(Sleep.SLEEP_COST)
