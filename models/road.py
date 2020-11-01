from models.lane import Lane
from models.turning import Turning


class Road(object):
    """
    Road that connects two intersections and has lanes at the end.
    """
    def __init__(self, origin, destination, end_direction, length):
        # The intersection at the start of the road
        self.origin = origin
        # The intersection that is at the end of the road
        self.destination = destination

        # The lanes at the end of the road
        self.lanes = {}

        # The direction at which we enter the destination
        self.end_direction = end_direction

        # The road is divided into length sections
        self.sections = [[] for _ in range(length)]

    def __repr__(self):
        return "Road[{} -> {}; lanes: {}]".format(self.origin, self.destination, self.lanes)

    def add_lane(self, turning: Turning, max_vehicles_per_step: int, road):
        """
        Add an incoming lane at incoming[direction,turning]
        """
        self.lanes[turning] = Lane(self.end_direction, turning, max_vehicles_per_step, road)

    def enter(self, vehicle):
        """
        Enter (at the start of) the road.
        """
        self.sections[0].append(vehicle)

    def last_section(self):
        """
        Return the last section
        """
        return self.sections[-1]

    def get_lanes_with_traffic_lights(self):
        """
        Returns a list of lanes that have a traffic light.
        """
        lanes = []
        for lane in self.lanes:
            if lane.has_traffic_light:
                lanes.append(lane)
        return lanes

    def has_traffic_lights(self):
        """
        Returns True if this road has traffic lights, which is the case when at least one of the lanes have a traffic
        light, False otherwise.
        """
        return len(self.get_lanes_with_traffic_lights()) > 0

    def update(self):
        """
        Update the vehicles that are driving on this road. All vehicles move one section further, which can be
        implemented by popping the last section and append a new section. This way the sections shift to the right
        and the order of the vehicles is preserved (no overtaking can happen). Vehicles that are on the final section
        are at the and of the road and get of the road to enter a lane.
        """
        # Keep track of how many vehicles finished
        num_finished = 0

        # The vehicles on the final section have reached the end of the road
        for vehicle in self.sections.pop():
            vehicle.roads_to_drive -= 1
            # If it is not finished yet, it chooses a lane to enter
            if not vehicle.is_finished():
                vehicle.choose_lane()
                if vehicle.lane.has_traffic_light:
                    vehicle.number_of_encountered_traffic_lights += 1
            else:
                num_finished += 1

        # All other vehicles move one section further
        for section in self.sections:
            for vehicle in section:
                vehicle.steps_driving += 1

        # Add an empty first section
        self.sections.append([])

        return num_finished

    def reset(self):
        """
        Reset the road by removing all vehicles from the sections
        """
        for section in self.sections:
            del section[:]
