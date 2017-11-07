

class TurnTracker(object):

    FAIRY = 0
    AI = 1

    def __init__(self, state):

        self.state = state

        cls = TurnTracker

        self.turn = cls.FAIRY

    def end_turn(self):

        self.turn = TurnTracker.AI

    def end_ai_turn(self):

        self.turn = TurnTracker.FAIRY
        self.state.start_of_turn()

    @property
    def ai_turn(self):
        return self.turn == TurnTracker.AI

    @property
    def fairy_turn(self):
        return self.turn == TurnTracker.FAIRY
