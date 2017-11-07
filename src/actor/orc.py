from map_object import MapObject
from image_components.animated_image_component import AnimatedImageComponent
from ai.orc_ai_component import OrcAIComponent
from random import choice
from actor import Actor


class Orc(Actor):

    DAMAGE_RANGE = (0, 2, 2, 2, 3, 1, 1)

    def __init__(self, state, coord):

        Actor.__init__(self, state, 'orc', coord)
        self.flag = MapObject.ACTOR
        self.blocks = True
        self.ai_component = self.set_ai()

    def set_image_component(self):
        return AnimatedImageComponent(self, self.key, transparent=True)

    def set_ai(self):
        return OrcAIComponent(self)

    def difficult_terrain(self):

        self.ai_component.use_action()

    def assault(self, point):

        mushlock = filter(lambda x: x.coord == point, self.state.object_list.get_all('mushlock'))
        if mushlock:
            self.attack(mushlock[0])
            self.ai_component.use_action(5)
        else:
            self.move(point)

    def attack(self, mush):
        self.animation = self.set_bump_animation(mush.coord)
        damage = choice(Orc.DAMAGE_RANGE)
        mush.take_damage(damage)
        if mush.ai_component.health <= 0:
            self.state.mushlock_ai_overlord.mushlock_slain()

    def take_damage(self, d):
        die = self.ai_component.take_damage(d)
        self.ai_component.engaged += 1
        if die:
            self.die()

    def die(self):
        self.state.object_list.remove_object(self)
        self.state.score_keeper.add_orc_kill()
