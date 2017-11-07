from random import shuffle


class FightTargeting(object):

    AGGRO = 3

    @classmethod
    def orc_in_aggro(cls, actor):

        coord = actor.coord
        object_list = actor.state.object_list

        orcs = object_list.get_all('orc')

        return cls.in_aggro(coord, orcs)

    @classmethod
    def mushlock_in_aggro(cls, actor):

        state = actor.state

        coord = actor.coord
        object_list = state.object_list

        mushlocks = object_list.get_all('mushlock')

        return cls.in_aggro(coord, mushlocks)

    @classmethod
    def in_aggro(cls, (x, y), objects):

        aggro = set()

        for ax in range(x-cls.AGGRO, x+cls.AGGRO+1):
            for ay in range(y-cls.AGGRO, y+cls.AGGRO+1):
                aggro.add((ax, ay))

        return filter(lambda x: x.coord in aggro, objects)

    @classmethod
    def get_next_step_to_orc(cls, actor, enemies):

        object_list = actor.state.object_list
        terrain = actor.state.terrain_map

        # returns the next point to move to

        d_map = cls.get_dijkstra(enemies, actor, object_list, terrain)

        adj = terrain.get_passable_adj(actor.coord)
        values = {}
        for point in adj:
            value = d_map.get(point, None)
            if value is not None:
                values[point] = value

        if values:
            move = cls.find_best_move(values)
        else:
            move = actor.coord
        return move

    @classmethod
    def get_dijkstra(cls, enemies, actor, object_list, terrain):

        edge = map(lambda x: x.coord, enemies)
        last_point = actor.coord

        blocked = set(map(lambda x: x.coord, object_list.get_blockers()))

        d_map = {}

        touched = set()
        value = 0

        while edge:
            for point in edge:
                touched.add(point)
                if d_map.get(point) is None:
                    d_map[point] = value
                elif value < d_map.get(point):
                    d_map[point] = value

            if last_point in touched:
                break

            next_edge = cls.get_next_edge(edge, terrain)
            edge = list(filter(lambda x: x not in blocked and x not in touched, next_edge))

            value += 1

        return d_map

    @classmethod
    def get_next_edge(cls, edge, terrain):

        next_edge = set()

        for point in edge:
            adj = terrain.get_passable_adj(point)
            for a in adj:
                next_edge.add(a)
        return list(next_edge)

    @classmethod
    def find_best_move(cls, values):

        keys = values.keys()
        shuffle(keys)
        weighted = sorted(keys, key=lambda x: values[x])

        return weighted[0]

    @classmethod
    def get_next_step_to_mushlock(cls, actor, enemies):

        object_list = actor.state.object_list
        terrain = actor.state.terrain_map

        # returns the next point to move to

        d_map = cls.get_dijkstra(enemies, actor, object_list, terrain)

        adj = terrain.get_passable_adj(actor.coord)
        values = {}
        for point in adj:
            value = d_map.get(point, None)
            if value is not None:
                values[point] = value

        if values:
            move = cls.find_best_move(values)
        else:
            move = actor.coord
        return move
