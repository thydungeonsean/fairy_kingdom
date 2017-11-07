from ai_component import AIComponent
from random import randint


class OrcAIComponent(AIComponent):

    NUM_ACTIONS = 4

    ASSAULT_THRESHOLD = 1000
    MIN_START_RAGE = 500
    MAX_START_RAGE = 1000

    RAGE_INCREASE = 5

    def __init__(self, owner):

        AIComponent.__init__(self, owner)

        self.health = randint(8, 12)
        self.rage = randint(OrcAIComponent.MIN_START_RAGE, OrcAIComponent.MAX_START_RAGE)

        self.actions = OrcAIComponent.NUM_ACTIONS
        self.foe = None
        self.engaged = 0

    def set_foe(self, foe):
        self.foe = foe

    def reset(self):
        self.actions = OrcAIComponent.NUM_ACTIONS
        if self.in_battle:
            self.engaged -= 1
            if self.engaged < 0:
                self.engaged = 0

    @property
    def in_battle(self):
        return self.engaged >= 1

    def use_action(self, num=1):
        self.actions -= num
        self.rage += randint(1, OrcAIComponent.RAGE_INCREASE)

    def get_next_behaviour(self):

        if self.engaged:
            return AIComponent.ORC_ASSAULT
        elif self.rage >= OrcAIComponent.ASSAULT_THRESHOLD:
            if self.houses_remain():
                return AIComponent.DESTROY
            else:
                return AIComponent.ORC_ASSAULT
        elif self.hidden():
            return AIComponent.LURK
        else:
            if randint(0, 10) < 1:
                return AIComponent.LURK
            else:
                return AIComponent.ORC_WANDER

    def take_damage(self, d):

        self.health -= d
        return self.health <= 0

    def houses_remain(self):
        return self.owner.state.object_list.houses_remain

    def hidden(self):
        return self.owner.state.shroud.point_is_hidden(self.owner.coord)