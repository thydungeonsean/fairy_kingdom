from behaviours.wander import Wander
from behaviours.eat import Eat
from behaviours.return_behaviour import Return
from behaviours.sleep import Sleep
from behaviours.orc_wander import OrcWander
from behaviours.destroy import Destroy
from behaviours.orc_lurk import Lurk
from behaviours.mine import Mine
from behaviours.defend import Defend
from behaviours.orc_assault import OrcAssault


class BehaviourList(object):

    WANDER = 0
    RETURN = 1
    DEFEND = 2
    MINE = 3
    SLEEP = 4
    EAT = 5

    RETREAT = 6
    LURK = 7
    ORC_WANDER = 8
    DESTROY = 9
    ORC_ASSAULT = 10

    dict = {
            WANDER: Wander(),
            EAT: Eat(),
            RETURN: Return(),
            SLEEP: Sleep(),
            DEFEND: Defend(),
            MINE: Mine(),

            RETREAT: Lurk(),
            LURK: Lurk(),
            ORC_WANDER: OrcWander(),
            DESTROY: Destroy(),
            ORC_ASSAULT: OrcAssault(),
            }

    @classmethod
    def get_behaviour(cls, key):

        return cls.dict[key]
