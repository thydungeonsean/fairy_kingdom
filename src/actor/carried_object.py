from map_object import MapObject


class CarriedObject(MapObject):

    def __init__(self, state, key):
        MapObject.__init__(self, state, key, (0, 0))
        self.carrier = None

    def pick_up(self, carrier):
        self.carrier = carrier

    @property
    def coord(self):
        return self.carrier.coord

    def put_down(self):
        self.carrier = None
