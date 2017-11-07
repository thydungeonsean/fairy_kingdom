

class Effect(object):

    def __init__(self, actor):

        self.actor = actor
        self.effect_handler = None

        self.speed = self.initialize_speed()
        self.tick = self.initialize_tick()

    def initialize_tick(self):
        raise NotImplementedError

    def initialize_speed(self):
        raise NotImplementedError

    def set_effect_handler(self, handler):
        self.effect_handler = handler

    def run(self):

        if self.tick % self.speed == 0:

            self.run_effect()

        self.tick += 1

    def die(self):
        self.effect_handler.remove_effect(self)

    def draw(self, surface):
        pass

    def run_effect(self):
        pass
