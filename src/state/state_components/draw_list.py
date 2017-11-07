

class DrawList(object):

    OBJECT = 0
    ACTOR = 1

    def __init__(self, state):

        self.actor_draw_list = []
        self.object_draw_list = []
        self.state = state

    def sort_actor_list(self):

        self.actor_draw_list = sorted(self.actor_draw_list, key=self.sort_by_y)

    @staticmethod
    def sort_by_y(actor):
        return actor.coord[1]

    def add_new(self, obj, flag):
        if flag == DrawList.OBJECT:
            self.add_object(obj)
        else:
            self.add_actor(obj)

    def remove_from_list(self, obj, flag):
        if flag == DrawList.OBJECT:
            self.remove_object(obj)
        else:
            self.remove_actor(obj)

    def add_actor(self, actor):
        self.actor_draw_list.append(actor)
        self.sort_actor_list()

    def remove_actor(self, actor):
        self.actor_draw_list.remove(actor)

    def add_object(self, o):
        self.object_draw_list.append(o)

    def remove_object(self, o):
        self.object_draw_list.remove(o)

    def draw(self, surface):

        for obj in self.object_draw_list:
            if self.object_visible(obj):
                obj.draw(surface)

        for actor in self.actor_draw_list:

            if self.object_visible(actor):
                actor.draw(surface)

    def object_visible(self, actor):

        return self.state.view.coord_in_view(actor.coord) and not self.state.shroud.point_is_hidden(actor.coord)
