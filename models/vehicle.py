import random

from models.direction import Direction
from models.intersection import Intersection
from models.light import Light
from models.turning import Turning
from models.waiting_queue import WaitingQueue


class Vehicle(object):
    """
    A Vehicle drives from intersection to intersection and does so in a number of steps.
    """
    waiting_queue: WaitingQueue

    def __init__(self, roads_to_drive, origin_direction: Direction, location: Intersection):
        self.roads_to_drive = roads_to_drive
        self.current_location = location
        self.origin_direction = origin_direction
        self.turning = self.get_turning()

        self.steps_driving = 0
        self.steps_waiting = 0
        self.number_of_encountered_traffic_lights = 0

    def is_finished(self):
        """
        Returns true if the vehicle is done driving
        """
        return self.roads_to_drive == 0

    def can_drive(self):
        """
        Return True if the vehicle can drive, False otherwise.
        """
        # If there are no traffic lights at the current intersection, the vehicle can always drive.
        if not self.current_location.has_traffic_lights:
            return True

        # If the traffic light is red, it cannot drive.
        if self.waiting_queue.traffic_light == Light.RED:
            return False

        # If the traffic light is GREEN but the vehicle is waiting too far in the back of the queue, it cannot drive.
        if not self.waiting_queue.can_drive_this_step(self):
            return False

        # In any other case, the vehicle can drive.
        return True

    def total_steps(self):
        """
        Return the total number of steps = steps_driving + steps_waiting.
        """
        return self.steps_driving + self.steps_waiting

    def get_turning(self):
        """
        Get the next turning (one of the (max) three lanes)
        """
        possible_turnings = [turning for turning in Turning
                             if self.current_location.incoming[self.origin_direction][turning] is not None]

        return random.choice(possible_turnings)

    def move_vehicle(self):
        """
        Update the states of the models to move the vehicle.
        :return: Whether the vehicle arrived at its destination
        """
        # Compute the next direction by taking a turn from the current direction
        next_direction = self.origin_direction.turn(self.turning)
        # The next intersection is at the outgoing lane at next_direction
        next_intersection = self.current_location.outgoing[next_direction]

        # Remove the vehicle from the current intersection and add it to the next.
        self.waiting_queue.queue.remove(self)

        # Update the location.
        self.current_location = next_intersection
        self.origin_direction = next_direction.opposite()
        self.turning = self.get_turning()
        self.waiting_queue = self.current_location.incoming[self.origin_direction][self.turning]
        self.waiting_queue.queue.append(self)

        # Update the number of roads the vehicle still has to drive.
        # TODO: account for the ROAD_LENGTH
        self.roads_to_drive -= 1

        # Remove the vehicle from the grid if it reached its destination and return True.
        if self.is_finished():
            self.waiting_queue.queue.remove(self)
            return True

        # Increment number of encountered traffic lights
        self.number_of_encountered_traffic_lights += next_intersection.has_traffic_lights

        return False
