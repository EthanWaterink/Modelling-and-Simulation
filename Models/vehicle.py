import random

from Models.direction import Direction
from Models.intersection import Intersection


class Vehicle(object):
    """Vehicle object"""
    last_location: Intersection

    def __init__(self, roads_to_drive, origin_direction, location: Intersection):
        self.roads_to_drive = roads_to_drive
        self.origin_direction = origin_direction
        self.current_location = location
        self.next_direction = self.get_next_direction()
        self.steps_driving = 0

        self.number_of_encountered_traffic_lights = 0
        self.waiting_steps = 0

    def get_next_direction(self):
        possible_directions = [self.current_location.outgoing.index(lane) for lane in self.current_location.outgoing if
                               lane]

        # If there are more possible directions than one, don't choose the direction the vehicle came from.
        if len(possible_directions) > 1:
            possible_directions.remove(self.origin_direction)

        return random.choice(possible_directions)

    def can_drive(self, max_vehicles_per_step):
        # If there are no traffic lights at the current intersection, the vehicle can always drive.
        if not self.current_location.has_traffic_lights():
            return True

        # If the traffic light is red, it cannot drive.
        if self.origin_direction != self.current_location.current_direction_green:
            return False

        # If the traffic light is green but the car is waiting too far in the back of the queue, it cannot drive.
        return self.current_location.vehicles[self.origin_direction].index(self) < max_vehicles_per_step

    def move_vehicle(self):
        """
        Update the states of the models to move the vehicle.
        :return: Whether the vehicle arrived at its destination
        """
        current_intersection = self.current_location
        next_intersection = current_intersection.outgoing[self.next_direction]

        # Remove the vehicle from the current intersection and add it to the next.
        current_intersection.vehicles[current_intersection.current_direction_green].remove(self)
        next_intersection.vehicles[Direction.opposite_direction(self.next_direction)].append(self)

        # Update the location.
        self.last_location = self.current_location
        self.current_location = next_intersection
        self.origin_direction = Direction.opposite_direction(self.next_direction)
        self.next_direction = self.get_next_direction()
        self.number_of_encountered_traffic_lights += next_intersection.has_traffic_lights()

        # Update the number of roads the vehicle still has to drive.
        self.roads_to_drive -= 1

        return self.roads_to_drive == 0
