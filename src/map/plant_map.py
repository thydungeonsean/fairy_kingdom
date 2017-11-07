from src.actor.plant import Plant


class PlantMap(object):

    def __init__(self, state):

        self.state = state
        self.plant_map = {}
        self.static_plant = Plant(self.state, (-1, -1))

    def add_plant(self, (x, y)):
        self.plant_map[(x, y)] = True

    def get_plant(self, (x, y)):
        return self.plant_map.get((x, y), False)

    def draw(self, surface):

        for x, y in self.plant_map.iterkeys():
            self.static_plant.move((x, y))
            if self.state.draw_list.object_visible(self.static_plant):
                self.static_plant.draw(surface)

    def harvest_plant(self, (x, y)):

        del self.plant_map[(x, y)]

    def clear_plant(self, (x, y)):
        if self.get_plant((x, y)):
            self.harvest_plant((x, y))
