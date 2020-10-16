import random
from typing import List, Tuple

from models.direction import Direction
from models.turning import Turning
from models.waiting_queue import WaitingQueue


class Intersection(object):
    """
    An Intersection is a position on the grid at [y,x] and contains the incoming and outgoing lanes.
    """
    incoming: List[List[WaitingQueue]]

    def __init__(self, y, x):
        # The incoming lanes, one per Turning for each Direction
        self.incoming = [[None for _ in Turning] for _ in Direction]
        # The outgoing lanes, one for each Direction
        self.outgoing = [None for _ in Direction]

        # Position [y,x] on the grid
        self.y = y
        self.x = x

        self.has_traffic_lights = False

        # TODO: Traffic Light Model dependent variables should probably be decoupled
        # Used for the Clock Model.
        self.current_direction_green = None

    def __repr__(self):
        return "Intersection[{},{}]".format(self.y, self.x)

    def num_vehicles_waiting(self):
        """
        Returns the number of vehicles that are currently waiting at this intersection
        """
        return sum(
            [len(waiting_queue.queue) for direction in self.incoming for waiting_queue in direction if waiting_queue])

    def add_outgoing_lane(self, goal_intersection, direction: Direction):
        """
        Add an outgoing lane to goal_intersection, which is at direction
        """
        self.outgoing[direction] = goal_intersection

    def add_incoming_lanes(self, direction: Direction, turning: Turning, max_vehicles_per_step: int):
        """
        Add an incoming lane at incoming[direction,turning]
        """
        self.incoming[direction][turning] = WaitingQueue(direction, turning, max_vehicles_per_step)

    def add_traffic_lights(self):
        """
        Add traffic lights to all waiting queues.
        """
        self.has_traffic_lights = True

        for (D, T) in [(D, T) for D in Direction for T in Turning]:
            if (waiting_queue := self.incoming[D][T]) is not None:
                waiting_queue.has_traffic_light = True

    def required_traffic_lights(self):
        """
        Returns True if this intersections requires traffic lights, which is the case for 3-way and 4-way
        intersections. False otherwise
        """
        return sum(1 for out in self.outgoing if out is not None)

    def get_random_waiting_queue(self):
        """
        Return a random waiting queue
        """
        possible_waiting_queues = []

        for (D, T) in [(D, T) for D in Direction for T in Turning]:
            if self.incoming[D][T] is not None:
                possible_waiting_queues.append((D, T))

        waiting_queue: Tuple[Direction, Turning] = random.choice(possible_waiting_queues)

        return waiting_queue
