from map_object import MapObject
from src.actor.ai.mushlock_ai_component import MushlockAIComponent
from src.actor.image_components.mushlock_image_component import MushlockImageComponent
from random import choice
from actor import Actor


class Mushlock(Actor):

    DAMAGE_RANGE = (0, 1, 1, 1, 1, 2)
    PICK_DAMAGE_RANGE = (1, 1, 1, 1, 2, 2)
    SPEAR_DAMAGE_RANGE = (1, 1, 2, 2, 2, 3)

    def __init__(self, state, coord):

        Actor.__init__(self, state, 'mushlock', coord)

        self.flag = MapObject.ACTOR
        self.blocks = True
        self.ai_component = self.set_ai()
        self.carried = None
        self.sleeping = False
        self.pouch = None

    def set_image_component(self):
        return MushlockImageComponent(self)

    def move(self, new):
        self.wake_up()
        self.harvest(new)
        touched = self.state.object_list.get_touched(self, new)
        self.animation = self.set_move_animation(new)
        self.coord = new
        for obj in touched:
            obj.on_mushlock(self)

        self.explore()

    def set_ai(self):

        return MushlockAIComponent(self)

    def explore(self):
        coords = []
        cx, cy = self.coord
        for y in range(cy-1, cy+2):
            for x in range(cx-1, cx+2):
                coords.append((x, y))
        self.state.shroud.explore_list(coords)

    def pick_up(self, object):
        if not self.carrying:
            self.carried = object
            self.image_component.update_carried()
            return True
        return False

    def consume_food(self):
        self.carried = None
        self.image_component.update_carried()

    @property
    def carrying(self):
        return self.carried is not None

    def harvest(self, point):

        if self.state.plant_map.get_plant(point) and not self.carrying:
            self.state.plant_map.harvest_plant(point)
            self.pick_up_food()

    def pick_up_food(self):
        return self.pick_up('food')

    def pick_up_gem(self):
        return self.pick_up('carried_gem')

    def pick_up_pick(self):
        return self.pick_up('carried_pick')

    def pick_up_spear(self):
        picked_up = self.pick_up('carried_spear')
        if picked_up:
            self.ai_component.health += 2  # make armed mushlocks a little more resilient
        return picked_up

    def fall_asleep(self):
        self.put_in_pouch()
        self.sleeping = True
        self.image_component.update_sleep()

    def wake_up(self):
        self.take_out_of_pouch()
        self.sleeping = False
        self.image_component.update_sleep()

    def tire_out(self):
        self.ai_component.fatigue += 100
        self.fall_asleep()

    def difficult_terrain(self):
        self.ai_component.fatigue += 1
        self.ai_component.use_action()

    def take_damage(self, d):
        die = self.ai_component.take_damage(d)
        if die:
            self.die()

    @property
    def armed(self):
        return self.carried == 'carried_spear'

    @property
    def miner(self):
        return self.carried == 'carried_pick'

    def attack(self, orc):
        self.animation = self.set_bump_animation(orc.coord)
        if self.armed:
            damage = choice(Mushlock.SPEAR_DAMAGE_RANGE)
        elif self.miner:
            damage = choice(Mushlock.PICK_DAMAGE_RANGE)
        else:
            damage = choice(Mushlock.DAMAGE_RANGE)
        orc.take_damage(damage)

    def drop(self):

        self.carried = None
        self.image_component.update_carried()

    def put_in_pouch(self):

        if self.carried is not None and self.carried in ('carried_spear', 'carried_pick', 'carried_gem', 'food'):
            self.pouch = self.carried
            self.carried = None
            self.image_component.update_carried()

    def take_out_of_pouch(self):

        if self.pouch is not None:
            self.carried = self.pouch
            self.pouch = None
            self.image_component.update_carried()

    def die(self):
        self.state.object_list.remove_object(self)
        self.state.object_creator.mushlocks -= 1
        self.state.score_keeper.subtract_mushlock()

    def drop_pick(self):
        self.carried = None
        self.state.object_creator.add_pick(self.coord)
