import random


class Vehicle(object):
    """
    A Vehicle drives from intersection to intersection and does so in a number of steps.
    """
    def __init__(self, roads_to_drive, road, lane):
        # The road the vehicle is driving on
        self.road = road
        # The lane the vehicle leaves the road
        self.lane = lane
        # Add the vehicle to the lane.
        lane.enter(self)

        # The number of roads to drive
        self.roads_to_drive = roads_to_drive

        # The number of steps driving
        self.steps_driving = 0
        # The number of steps waiting
        self.steps_waiting = 0
        # The number of traffic lights encountered
        self.number_of_encountered_traffic_lights = 1 if lane.has_traffic_light else 0

        # Used for resetting
        self.start_lane = lane
        self.start_road = road
        self.start_roads_to_drive = roads_to_drive

    def is_finished(self):
        """
        Returns true if the vehicle is done driving
        """
        return self.roads_to_drive == 0

    def total_steps(self):
        """
        Return the total number of steps = steps_driving + steps_waiting.
        """
        return self.steps_driving + self.steps_waiting

    def choose_lane(self):
        """
        Choose a random lane and enter it
        """
        lane = random.choice(list(self.road.lanes.values()))
        lane.enter(self)
        self.lane = lane

    def cross_intersection(self):
        """
        Cross the intersection and enter the road
        """
        self.lane.goes_to_road.enter(self)
        self.road = self.lane.goes_to_road

    def reset(self):
        """
        Reset the vehicle by repositioning it and setting the starting values
        """
        self.lane = self.start_lane
        self.lane.enter(self)
        self.road = self.start_road
        self.roads_to_drive = self.start_roads_to_drive

        self.steps_waiting = 0
        self.steps_driving = 0
        self.number_of_encountered_traffic_lights = 1 if self.lane.has_traffic_light else 0
