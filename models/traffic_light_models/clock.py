import random

from models.traffic_light_models.traffic_light_models import *
from models.direction import Direction
from models.turning import Turning


class Clock(TrafficLightModel):
    """
    The Clock model
    """
    def __init__(self, grid):
        # For every intersection (with a traffic light) keep track which direction is currently green
        self.current_direction_green = {}
        # Choose random direction to start with (from the possible lanes)
        for intersection in grid.all_intersections_with_traffic_lights():
            self.current_direction_green[intersection] = random.choice(list(intersection.incoming_roads.keys()))

        # Keep track if this is the first time calling the update method.
        self.is_first_time_calling = True

    def update(self, intersection: Intersection):
        """
        Update the intersection with the Clock model.
        """
        def lanes_to_change(direction):
            """
            Get the lanes that need to be changed, which are the lanes at direction, and the right lane at the next
            direction
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

        # If this method is called for the first time, turn all lights GREEN at the starting direction.
        if self.is_first_time_calling:
            # Set all traffic lights at the current direction to GREEN.
            for lane in lanes_to_change(self.current_direction_green[intersection]):
                lane.set_traffic_light_state(Light.GREEN)
            self.is_first_time_calling = False
            return

        # Set all traffic lights at the current direction to RED.
        for lane in lanes_to_change(self.current_direction_green[intersection]):
            lane.set_traffic_light_state(Light.RED)

        # Go to the next direction
        self.current_direction_green[intersection] = self.current_direction_green[intersection].next()
        # If there is no incoming road at the next direction, go to the next. Note that there are at most two more
        # next directions and it will be one of those two, because an intersection with one incoming road does not
        # require traffic lights.
        while self.current_direction_green[intersection] not in intersection.incoming_roads:
            self.current_direction_green[intersection] = self.current_direction_green[intersection].next()

        # Set all traffic lights at the new direction to GREEN.
        for lane in lanes_to_change(self.current_direction_green[intersection]):
            lane.set_traffic_light_state(Light.GREEN)