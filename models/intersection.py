import random

from models.direction import Direction
from models.road import Road


class Intersection(object):
    """
    An Intersection is a position on the grid at [y,x] and contains the incoming and outgoing lanes.
    """
    def __init__(self, x, y):
        # The outgoing roads
        self.outgoing_roads = {}
        # The incoming roads
        self.incoming_roads = {}

        # Position [x,y] on the grid
        self.x = x
        self.y = y

        # True if this intersection has traffic lights, False otherwise
        self.has_traffic_lights = False

        # The traffic light length of the traffic lights at this intersection (if they exist)
        self.traffic_light_length = None

    def __repr__(self):
        return "Intersection[{},{}]".format(self.x, self.y)

    def position(self):
        """
        Return the position tuple (x, y)
        """
        return self.x, self.y

    def num_vehicles_waiting(self):
        """
        Returns the number of vehicles that are currently waiting at this intersection
        """
        return sum([len(lane.queue) for lane in self.get_all_lanes()])

    def add_road(self, goal_intersection, direction: Direction):
        """
        Add an outgoing lane to goal_intersection, which is at direction
        """
        road = Road(self, goal_intersection, direction.opposite())
        self.outgoing_roads[direction] = road
        goal_intersection.incoming_roads[direction.opposite()] = road

    def get_all_lanes(self):
        """
        Get all the lanes at this intersection (by getting the lanes of the incoming roads).
        """
        lanes = []
        for inc_road in self.incoming_roads.values():
            for lane in inc_road.lanes.values():
                lanes.append(lane)
        return lanes

    def get_all_lanes_with_traffic_lights(self):
        """
        Get all lanes at this intersection that have a traffic light.
        """
        lanes_with_traffic_lights = []
        for lane in self.get_all_lanes():
            if lane.has_traffic_light:
                lanes_with_traffic_lights.append(lane)
        return lanes_with_traffic_lights

    def get_all_lanes_with_vehicles(self):
        """
        Get all lanes that have at least one vehicle.
        """
        lanes_with_vehicles = []
        for lane in self.get_all_lanes():
            if lane.has_vehicles():
                lanes_with_vehicles.append(lane)
        return lanes_with_vehicles

    def get_random_lane(self):
        """
        Return a random waiting queue
        """
        return random.choice(self.get_all_lanes())
