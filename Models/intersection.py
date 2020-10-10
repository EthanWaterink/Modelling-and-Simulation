import random
from typing import List, Tuple

from Models.direction import Direction, get_lane_number
from Models.light import Light
from Models.waiting_queue import WaitingQueue


class Intersection(object):
    """Intersection object"""
    incoming: List[List[WaitingQueue]]

    def __init__(self, y, x, default_direction_green: Direction):
        # An intersection has a maximum of 4 connected neighbours (one for each direction).
        self.incoming = [[None, None, None], [None, None, None], [None, None, None], [None, None, None]]
        self.outgoing = 4 * [None]

        # Position [y,x] on the grid
        self.y = y
        self.x = x

        self.has_traffic_lights = False

        # Used for the Clock Model.
        self.current_direction_green = None

    def __str__(self):
        return "Intersection[" + str(self.y) + "," + str(self.x) + "]"

    def num_vehicles_waiting(self):
        return sum(
            [len(waiting_queue.queue) for direction in self.incoming for waiting_queue in direction if waiting_queue])

    def add_outgoing_lane(self, goal_intersection, direction):
        # Add the outgoing lane to the list.
        self.outgoing[direction] = goal_intersection

        # Make it possible for every incoming direction to go to the newly added direction.
        for incoming_direction in range(4):
            if len([lane for lane in self.incoming[incoming_direction] if lane]) == 0:
                continue

            self.incoming[incoming_direction][Direction.get_lane_number(incoming_direction, direction)] = WaitingQueue()

    def add_incoming_lane(self, direction):
        # For each outgoing lane of the intersection, add a incoming lane from the current direction.
        for outgoing_direction in range(4):
            if self.outgoing[outgoing_direction] is None or direction == outgoing_direction:
                continue

            self.incoming[direction][get_lane_number(direction, outgoing_direction)] = WaitingQueue()

    def add_traffic_lights(self):
        self.has_traffic_lights = True

        for incoming_direction in range(4):
            for lane_number in range(3):
                if (waiting_queue := self.incoming[incoming_direction][lane_number]) is not None:
                    waiting_queue.has_traffic_light = True

    def get_random_waiting_queue(self):
        possible_waiting_queues = []

        for incoming_direction in range(4):
            for lane_number in range(3):
                if self.incoming[incoming_direction][lane_number] is None:
                    continue

                possible_waiting_queues.append((incoming_direction, lane_number))

        waiting_queue: Tuple[int, int] = random.choice(possible_waiting_queues)

        return waiting_queue
