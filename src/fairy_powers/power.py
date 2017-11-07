

class Power(object):

    def __init__(self):
        self.state = None

    def load_state(self, state):
        self.state = state

    def point_is_valid(self, point):
        return True

    def use_power(self, point):
        pass
