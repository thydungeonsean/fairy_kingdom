

class ScoreKeeper(object):

    MAX_MUSHLOCK = 100
    MAX_HOUSE = 250
    FOOD = 1
    GEM = 50
    TURN = 10
    ORCS = 1000

    def __init__(self, state):

        self.state = state

        self.score = 0

        self.mushlocks = 0
        self.mushhouses = 0

        self.most_mushlocks = 0
        self.most_mushhouses= 0

        self.food = 0
        self.gems = 0

        self.turns = 0

        self.powers_used = 0

        self.orcs_slain = 0

    def compute_score(self):

        cls = ScoreKeeper

        self.score += self.most_mushlocks * cls.MAX_MUSHLOCK
        self.score += self.most_mushhouses * cls.MAX_HOUSE
        self.score += self.food * cls.FOOD
        self.score += self.gems * cls.GEM
        self.score += self.turns * cls.TURN
        self.score += self.orcs_slain * cls.ORCS

    def add_mushlock(self):

        if self.mushlocks + 1 > self.most_mushlocks:
            self.most_mushlocks += 1
        self.mushlocks += 1

    def add_house(self):

        if self.mushhouses + 1 > self.most_mushhouses:
            self.most_mushhouses += 1
        self.mushhouses += 1

    def subtract_mushlock(self):
        self.mushlocks -= 1

    def subtract_house(self):
        self.mushhouses -= 1

    def add_food(self):
        self.food += 1

    def add_gem(self):
        self.gems += 1

    def add_orc_kill(self):
        self.orcs_slain += 1

    def add_turn(self):
        self.turns += 1

    def add_power_use(self):
        self.powers_used += 1


