from collections import deque
import random

from models.traffic_light_models.traffic_light_models import *
from models.turning import Turning


class Clock(TrafficLightModel):
    """
    The Clock model.
    """
    def __init__(self, grid):
        # For every intersection (with a traffic light) store a deque of List[Lane], which are the lanes_to_change
        # for a direction
        self.lanes_per_direction = {}

        # Choose random direction to start with (from the possible incoming roads with traffic lights)
        for intersection in grid.all_intersections_with_traffic_lights():
            # Initialize the empty deque
            self.lanes_per_direction[intersection] = deque()
            # Check all incoming roads
            for D_inc, road_inc in intersection.incoming_roads.items():
                # Only keep the roads that have traffic lights
                if road_inc.has_traffic_lights:
                    self.lanes_per_direction[intersection].append(self.lanes_to_change(intersection, D_inc))

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
        if direction in (roads := intersection.incoming_roads):
            for lane_change in roads[direction].lanes.values():
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

        # If this method is called for the first time, turn all lights GREEN at a random direction.
        if self.is_first_time_calling:
            # Shuffle the deque, which determines the order in which they will turn GREEN.
            random.shuffle(self.lanes_per_direction[intersection])
            # Set all traffic lights at the current direction to GREEN.
            for lane in self.lanes_per_direction[intersection][0]:
                lane.set_traffic_light_state(Light.GREEN)
            self.is_first_time_calling = False
            return

        # Set all traffic lights at the current direction to RED.
        for lane in self.lanes_per_direction[intersection][0]:
            lane.set_traffic_light_state(Light.RED)

        # Go to the next direction
        self.lanes_per_direction[intersection].rotate(1)

        # Set all traffic lights at the new direction to GREEN.
        for lane in self.lanes_per_direction[intersection][0]:
            lane.set_traffic_light_state(Light.GREEN)
