from src.constants import *
from src.map.map_image import MapImage


class View(object):

    UPPER_LIMIT = -MapImage.PADDING
    LEFT_LIMIT = -MapImage.PADDING
    LOWER_LIMIT = MAP_H - DISPLAY_H + MapImage.PADDING + 1
    RIGHT_LIMIT = MAP_W - DISPLAY_W + MapImage.PADDING + 1

    def __init__(self, map_image):
    
        self.coord = (0, 0)
        self.map_image = map_image
        self.pressed = {'up': False, 'down': False, 'left': False, 'right': False}
        self.directions = self.pressed.keys()
        self.move = {'up': self.move_up, 'down': self.move_down, 'left': self.move_left, 'right': self.move_right}

        self.map_image.set_coord(self.set_map_coord())

    def press(self, d):
        self.pressed[d] = True

    def release(self, d):
        self.pressed[d] = False

    def run(self):

        for d in self.directions:
            if self.pressed[d]:
                self.move[d]()

    def set_coord(self, coord):
        if self.coord_in_limits(coord):
            self.coord = coord
            self.map_image.set_coord(self.set_map_coord())

    def move_up(self):
        
        x, y = self.coord
        self.set_coord((x, y-1))
        
    def move_down(self):
        
        x, y = self.coord
        self.set_coord((x, y+1))
        
    def move_right(self):
        
        x, y = self.coord
        self.set_coord((x+1, y))
        
    def move_left(self):
        
        x, y = self.coord
        self.set_coord((x-1, y))

    @classmethod
    def coord_in_limits(cls, (x, y)):
        return cls.LEFT_LIMIT <= x < cls.RIGHT_LIMIT and cls.UPPER_LIMIT <= y < cls.LOWER_LIMIT

    def set_map_coord(self):

        x_off = -MapImage.PADDING * TILEW
        y_off = -MapImage.PADDING * TILEH

        view_x, view_y = self.coord
        x_off -= view_x * TILEW
        y_off -= view_y * TILEH

        return x_off, y_off

    def coord_in_view(self, (x, y)):

        vx, vy = self.coord
        return vx <= x < vx + DISPLAY_W and vy <= y < vy + DISPLAY_H + 1

    def set_start_area(self, (x, y)):

        tlx = x - DISPLAY_W / 2
        tly = y - DISPLAY_H / 2

        if not self.coord_in_limits((tlx, tly)):
            tlx, tly = self.get_coord_in_limits((tlx, tly))

        self.set_coord((tlx, tly))

    @classmethod
    def get_coord_in_limits(cls, (x, y)):

        if cls.coord_in_limits((x, y)):
            return x, y

        if x < cls.LEFT_LIMIT:
            x += 1
        elif x >= cls.RIGHT_LIMIT:
            x -= 1

        if y < cls.UPPER_LIMIT:
            y += 1
        elif y >= cls.LOWER_LIMIT:
            y -= 1

        return cls.get_coord_in_limits((x, y))
