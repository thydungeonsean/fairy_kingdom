from behaviour_list import BehaviourList


class AIComponent(object):

    # mushlock
    WANDER = BehaviourList.WANDER
    RETURN = BehaviourList.RETURN
    DEFEND = BehaviourList.DEFEND
    MINE = BehaviourList.MINE
    SLEEP = BehaviourList.SLEEP
    EAT = BehaviourList.EAT

    # orc
    RETREAT = BehaviourList.RETREAT
    LURK = BehaviourList.LURK
    ORC_WANDER = BehaviourList.ORC_WANDER
    DESTROY = BehaviourList.DESTROY
    ORC_ASSAULT = BehaviourList.ORC_ASSAULT

    def __init__(self, owner):

        self.owner = owner
        self.behaviour = AIComponent.WANDER
        self.actions = 0

    def run(self):

        self.behaviour = self.get_next_behaviour()

        behaviour = BehaviourList.get_behaviour(self.behaviour)
        behaviour.run_behaviour(self)

    def reset(self):
        pass

    def use_action(self, num=1):
        self.actions -= num

    def get_next_behaviour(self):

        pass
