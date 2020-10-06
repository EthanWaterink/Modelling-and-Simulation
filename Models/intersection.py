from Models.direction import Direction


class Intersection(object):
    """Intersection object"""
    def __init__(self, y, x, default_direction_green: Direction):
        # An intersection has a maximum of 4 neighbours (one for each direction).
        self.incoming = [None, None, None, None]
        self.outgoing = [None, None, None, None]

        # Position [y,x] on the grid
        self.y = y
        self.x = x

        self.vehicles = [[], [], [], []]
        self.current_direction_green = default_direction_green

    def __str__(self):
        return "Intersection[" + str(self.y) + "," + str(self.x) + "]"

    def requires_traffic_lights(self):
        return sum([1 for lane in self.incoming if lane]) >= 3

    def num_cars_waiting(self):
        return sum([len(vehicles) for vehicles in self.vehicles])


