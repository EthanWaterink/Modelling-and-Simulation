import random

from Models.intersection import Intersection


class Vehicle(object):
    """Vehicle object"""
    last_location: Intersection

    def __init__(self, roads_to_drive, origin_direction, location: Intersection):
        self.roads_to_drive = roads_to_drive
        self.origin_direction = origin_direction
        self.current_location = location
        self.steps_driving = 0

    def get_next_direction(self):
        possible_directions = [self.current_location.outgoing.index(lane) for lane in self.current_location.outgoing if
                               lane]

        # If there are more possible directions than one, don't choose the direction the vehicle came from.
        if len(possible_directions) > 1:
            possible_directions.remove(self.origin_direction)

        return random.choice(
            [self.current_location.outgoing.index(lane) for lane in self.current_location.outgoing if lane])
