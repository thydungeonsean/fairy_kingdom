

class AIHandler(object):

    def __init__(self, state):

        self.state = state

    def run(self):

        ai_havers = self.state.object_list.get_ai_objects()
        moves_remaining = False

        for object in ai_havers:

            if object.ai_component.actions > 0:
                moves_remaining = True
                object.ai_component.run()

        if not moves_remaining:
            self.state.turn_tracker.end_ai_turn()
            self.reset_ais(ai_havers)

    def reset_ais(self, ai_havers):

        for obj in ai_havers:

            obj.ai_component.reset()
