from random import randint


class MushlockAIOverlord(object):

    PANIC_LEVEL = 15

    def __init__(self, state):

        self.state = state
        self.panic = 0

    def update_ai_state(self):
        self.panic -= 5
        if self.panic < 0:
            self.panic = 0

    def mushhouse_pillaged(self):
        self.panic += 10

    def mushlock_slain(self):
        self.panic += randint(0, 1)

    @property
    def is_panicked(self):
        return self.panic >= MushlockAIOverlord.PANIC_LEVEL
