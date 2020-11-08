from collections import deque
import random

from models.traffic_light_models.traffic_light_models import *
from models.turning import Turning


class Clock(TrafficLightModel):
    """
    The Clock model cycles through traffic light configurations.
    """
    def __init__(self):
        # For every intersection (with a traffic light) store a deque of List[Lane], which are the lanes_to_change
        # for a direction
        self.lanes_per_direction = {}

        # Used to check if the Update method is called for the first time or not
        self.is_first_time_calling = True

    def setup(self, grid):
        """
        Setup the Clock traffic light model.
        """
        self.lanes_per_direction = {}

        # Choose random direction to start with (from the possible incoming roads with traffic lights)
        for intersection in grid.all_intersections_with_traffic_lights():
            # Initialize the empty deque
            self.lanes_per_direction[intersection] = deque()
            # Check all incoming roads
            for inc_D, inc_road in intersection.incoming_roads.items():
                # Only keep the roads that have traffic lights
                if inc_road.has_traffic_lights:
                    self.lanes_per_direction[intersection].append(self.lanes_to_change(intersection, inc_D))

        # Keep track if this is the first time calling the update method.
        self.is_first_time_calling = True

    @staticmethod
    def lanes_to_change(intersection, direction):
        """
        Get the lanes that need to be changed, which are the lanes at direction, and the right lane at the next
        direction. Can be calculated once on initialization.
        """
        # List of lanes to change
        lanes = []

        # Get the lanes at this direction
        for lane_change in intersection.incoming_roads[direction].lanes.values():
            if lane_change.has_traffic_light:
                lanes.append(lane_change)

        # Go to the next direction
        next_direction = direction.next()

        # Get the RIGHT lane of the next direction
        if next_direction in (roads := intersection.incoming_roads):
            if Turning.RIGHT in (lanes_next := roads[next_direction].lanes.values()):
                if (lane_change := lanes_next[Turning.RIGHT]).has_traffic_light:
                    lanes.append(lane_change)

        return lanes

    def update(self, intersection: Intersection):
        """
        Update the intersection with the Clock model.
        """
        lanes = self.lanes_per_direction[intersection]
        # If this method is called for the first time, turn all lights GREEN at a random direction.
        if self.is_first_time_calling:
            # Shuffle the deque, which determines the order in which they will turn GREEN.
            random.shuffle(lanes)
            # Set all traffic lights at the current direction to GREEN.
            for lane in lanes[0]:
                lane.turn_green()
            self.is_first_time_calling = False
            return

        # Set all traffic lights at the current direction to RED.
        for lane in lanes[0]:
            lane.turn_red()

        # Go to the next direction
        lanes.rotate(1)

        # Set all traffic lights at the new direction to GREEN.
        for lane in lanes[0]:
            lane.turn_green()
