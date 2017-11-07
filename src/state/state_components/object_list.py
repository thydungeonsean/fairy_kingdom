from src.actor.map_object import MapObject


class ObjectList(object):

    def __init__(self, state):

        self.object_list = []
        self.state = state
        self.houses_remain = True

    def remove_object(self, obj):
        self.object_list.remove(obj)
        self.state.draw_list.remove_from_list(obj, obj.flag)

    def add_object(self, obj):
        self.object_list.append(obj)
        self.state.draw_list.add_new(obj, obj.flag)

    def run(self):
        for obj in self.object_list:
            obj.run()

    def point_is_blocked(self, point):

        points_blocked_by_object = set(map(lambda x: x.coord, filter(lambda x: x.blocks, self.object_list)))
        return point in points_blocked_by_object

    def get_all(self, key):
        if isinstance(key, tuple):
            return filter(lambda x: x.key in key, self.object_list)
        else:
            return filter(lambda x: x.key == key, self.object_list)

    def get_ai_objects(self):
        return filter(lambda x: x.flag == MapObject.ACTOR and x.ai_component is not None, self.object_list)

    def get_objects_at_coord(self, coord):

        return filter(lambda x: x.coord == coord, self.object_list)

    def get_touched(self, actor, coord):

        touched = self.get_objects_at_coord(coord)
        return filter(lambda x: x != actor, touched)

    def get_all_of_key_at_coord(self, key, coord):
        at_coord = self.get_objects_at_coord(coord)
        return filter(lambda x: x.key == key, at_coord)

    def get_blockers(self):
        return filter(lambda x: x.blocks, self.object_list)
