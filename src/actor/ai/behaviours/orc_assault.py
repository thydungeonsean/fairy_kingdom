from defend import Defend
from random import choice
from fight_targetting import FightTargeting


class OrcAssault(Defend):

    def __init__(self):
        Defend.__init__(self)

    def run_specifics(self):

        # try to attack who we attacked last time
        if self.ai_component.foe is not None and self.foe_alive() and self.fight_foe():
            return

        # try to attack anyone in range
        if self.try_to_engage():
            return

        possible_moves = self.get_passable_adj()
        possible_moves.append(self.actor.coord)

        move = choice(possible_moves)
        self.actor.move(move)
        self.ai_component.use_action()

    def fight_foe(self):

        adj = self.get_adj()
        if self.ai_component.foe.coord in adj:
            # if so, attack_foe
            self.actor.attack(self.ai_component.foe)
            # if foe is dead, set foe to None
            self.foe_alive()
            return True
        return False

    def try_to_engage(self):

        # is there an enemy in range?
        mushlocks = FightTargeting.mushlock_in_aggro(self.actor)
        if not mushlocks:
            return False  # no one in range, just be normal

        adj_enemies = self.get_adj_enemies(mushlocks)
        if adj_enemies:
            # is there an adj orc?
            # choose one, set as ai_component.foe
            foe = choice(adj_enemies)
            self.actor.attack(foe)
            if foe.ai_component.health > 0:
                self.ai_component.set_foe(foe)
            self.ai_component.use_action(Defend.ACTION_COST)

            return True

        else:  # no adj enemy, path find to one
            move = self.get_path_to_foe(mushlocks)
            self.actor.move(move)
            self.ai_component.use_action()

            return True

    def get_path_to_foe(self, mushlocks):

        return FightTargeting.get_next_step_to_mushlock(self.actor, mushlocks)

    def get_adj_enemies(self, enemies):
        adj = set(self.get_adj())
        adj_enemies = filter(lambda x: x.coord in adj, enemies)
        return adj_enemies

