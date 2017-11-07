from behaviour import Behaviour


class Eat(Behaviour):

    FOOD_VALUE = 20
    EAT_COST = 3

    def __init__(self):
        Behaviour.__init__(self)
        pass

    def run_specifics(self):

        self.eat()

    def eat(self):
        cls = Eat
        self.ai_component.hunger -= cls.FOOD_VALUE
        self.ai_component.starvation = 0
        self.actor.consume_food()
        self.ai_component.use_action(cls.EAT_COST)
