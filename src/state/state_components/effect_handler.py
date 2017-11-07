

class EffectHandler(object):

    def __init__(self, state):

        self.state = state
        self.effects = []

    def run(self):

        for effect in self.effects:
            effect.run()

    def add_effect(self, effect):
        self.effects.append(effect)
        effect.set_effect_handler(self)

    def remove_effect(self, effect):
        self.effects.remove(effect)

    def draw(self, surface):

        for effect in self.effects:
            effect.draw(surface)
