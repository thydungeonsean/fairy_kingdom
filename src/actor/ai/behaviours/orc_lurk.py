from behaviour import Behaviour


class Lurk(Behaviour):

    def __init__(self):

        Behaviour.__init__(self)

    def run_specifics(self):

        self.ai_component.use_action(6)
