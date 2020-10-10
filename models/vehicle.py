import random

from models.direction import Direction, get_opposite_direction, get_lane_number
from models.intersection import Intersection
from models.light import Light
from models.waiting_queue import WaitingQueue


class Vehicle(object):
    """Vehicle object"""
    last_location: Intersection
    waiting_queue: WaitingQueue

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
        if len(possible_directions) > 1 and self.origin_direction in possible_directions:
            possible_directions.remove(self.origin_direction)

        return random.choice(possible_directions)

    def can_drive(self, max_vehicles_per_step):
        # If there are no traffic lights at the current intersection, the vehicle can always drive.
        if not self.current_location.has_traffic_lights:
            return True

        # If the traffic light is red, it cannot drive.
        if self.waiting_queue.traffic_light == Light.RED:
            return False

        # If the traffic light is green but the car is waiting too far in the back of the queue, it cannot drive.
        # TODO: check in the current waiting queue whether the car can drive
        return True

    def move_vehicle(self):
        """
        Update the states of the models to move the vehicle.
        :return: Whether the vehicle arrived at its destination
        """
        current_intersection = self.current_location
        next_intersection = current_intersection.outgoing[self.next_direction]

        # Remove the vehicle from the current intersection and add it to the next.
        self.waiting_queue.queue.remove(self)

        # Update the location.
        self.last_location = self.current_location
        self.current_location = next_intersection
        self.origin_direction = get_opposite_direction(self.next_direction)
        self.next_direction = self.get_next_direction()
        self.waiting_queue = self.current_location.incoming[self.origin_direction][
            get_lane_number(self.origin_direction, self.next_direction)]
        self.waiting_queue.queue.append(self)
        self.number_of_encountered_traffic_lights += next_intersection.has_traffic_lights

        # Update the number of roads the vehicle still has to drive.
        self.roads_to_drive -= 1

        return self.roads_to_drive == 0
