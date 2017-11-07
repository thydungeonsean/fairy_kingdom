from ai_component import AIComponent
from random import randint
from src.constants import STUMP


class MushlockAIComponent(AIComponent):

    NUM_ACTIONS = 5

    SLEEP_THRESHOLD = 50
    MAX_FATIGUE = 150
    HUNGRY_THRESHOLD = 25
    MAX_HUNGER = HUNGRY_THRESHOLD * 3

    STARVATION_POINT = 20
    HIBERNATE_POINT = 15

    FOOD_VALUE = 20

    # action costs
    MOVE_COST = 1
    EAT_COST = 3

    def __init__(self, owner):

        AIComponent.__init__(self, owner)
        self.actions = MushlockAIComponent.NUM_ACTIONS

        self.hunger = 0
        self.fatigue = randint(0, 19)
        self.starvation = 0

        self.health = randint(1, 3)
        self.foe = None

    def set_foe(self, foe):
        self.foe = foe

    def reset(self):
        self.actions = MushlockAIComponent.NUM_ACTIONS

    def use_action(self, num=1):
        self.actions -= num
        if self.has_food or self.mining or self.armed:
            pass
        else:
            self.increase_hunger()
        self.increase_fatigue()

    def increase_fatigue(self):
        self.fatigue += 1
        self.fatigue = min((self.fatigue, MushlockAIComponent.MAX_FATIGUE))

    def increase_hunger(self):
        self.hunger += 1
        self.hunger = min((self.hunger, MushlockAIComponent.MAX_HUNGER))

    def starve(self):
        if self.hunger == MushlockAIComponent.MAX_HUNGER:
            self.starvation += 1

            if self.starvation >= MushlockAIComponent.STARVATION_POINT:
                self.owner.state.object_creator.stumpify(self.owner)
                self.owner.die()
            elif self.starvation >= MushlockAIComponent.HIBERNATE_POINT:
                self.fatigue += 10

    def get_next_behaviour(self):

        if self.sleeping:
            self.try_to_wake()

        if self.has_food:
            if self.hungry:
                return AIComponent.EAT
            else:
                return AIComponent.RETURN

        elif self.armed:
            return AIComponent.DEFEND

        elif self.has_gem:
            return AIComponent.RETURN

        elif self.sleeping:
            return AIComponent.SLEEP

        elif self.exhausted:
            if self.falling_asleep():
                return AIComponent.SLEEP
            else:
                return AIComponent.WANDER

        elif self.mining:
            if self.owner.state.mushlock_ai_overlord.is_panicked:
                #print 'mushlocks are in lockdown!!!'
                return AIComponent.DEFEND
            return AIComponent.MINE

        else:
            if self.owner.state.mushlock_ai_overlord.is_panicked:
                #print 'mushlocks are in lockdown!!!'
                return AIComponent.DEFEND
            return AIComponent.WANDER

    @property
    def has_food(self):
        return self.owner.carried == 'food'

    @property
    def has_gem(self):
        return self.owner.carried == 'carried_gem'

    @property
    def hungry(self):
        return self.hunger >= MushlockAIComponent.HUNGRY_THRESHOLD

    @property
    def exhausted(self):
        return self.fatigue >= MushlockAIComponent.SLEEP_THRESHOLD

    @property
    def sleeping(self):
        return self.owner.sleeping

    @property
    def mining(self):
        return self.owner.miner

    @property
    def armed(self):
        return self.owner.armed

    def try_to_wake(self):
        if self.fatigue <= 0:
            self.owner.wake_up()

    def falling_asleep(self):
        coord = self.owner.coord
        in_water = filter(lambda x: x.coord == coord, self.owner.state.object_list.get_all('water'))
        if not in_water:
            roll = randint(0, 99)
            return roll < self.fatigue
        return False

    def take_damage(self, d):

        self.health -= d
        return self.health <= 0
