from effect import Effect


# TODO - make a smooth gust animation effect
class GustEffect(Effect):

    GUST_SPEED = 2

    def __init__(self, actor, vector):

        Effect.__init__(self, actor)

        self.vector = vector
        self.moves = 3

    def initialize_tick(self):
        return GustEffect.GUST_SPEED

    def initialize_speed(self):
        return GustEffect.GUST_SPEED

    def run_effect(self):

        self.moves -= 1

        failed = self.try_to_move_actor()
        if failed:
            self.moves = 0

        if self.moves <= 0:
            self.die()

    def try_to_move_actor(self):

        vx, vy = self.vector
        tx, ty = self.actor.coord
        next_coord = tx + vx, ty + vy

        if self.actor.state.terrain_map.point_is_passable(next_coord) and \
                not self.actor.state.object_list.point_is_blocked(next_coord):
            self.actor.move(next_coord)

            return False
        return True
