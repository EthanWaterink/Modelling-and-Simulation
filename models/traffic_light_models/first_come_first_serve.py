import random

from models.traffic_light_models.traffic_light_models import *


class FirstComeFirstServe(TrafficLightModel):
    """
    Local optimum model with first come first serve basis.
    """
    def __init__(self):
        self.queues = {}

    def setup(self, grid):
        # For every intersection store a list (queue) of lanes
        self.queues = {}

        # Initialize the list
        for intersection in grid.all_intersections_with_traffic_lights():
            self.queues[intersection] = []

    def update(self, intersection: Intersection):
        """
        Update the intersection with the FirstComeFirstServe model.
        """
        # Get the queue of the intersection
        queue = self.queues[intersection]

        # The order in which vehicles arrive at the intersection is determined by the order which we call the
        # Lane.update. This would give an unfair advantage to those called first. Hence, given a list of lanes where
        # vehicles arrive, shuffle it so that the order is random. Only add lanes that are not already in the queue.
        random.shuffle(random_lane_order := intersection.get_all_lanes_with_vehicles())
        for lane in random_lane_order:
            if lane not in queue:
                queue.append(lane)

        # All traffic lights are set to RED.
        all_traffic_lights_red(intersection)

        # Make a copy of the queue.
        options = queue.copy()
        # Loop while there are still options.
        while len(options) > 0:
            # Get and remove the lane that entered first in the current options queue.
            lane = options.pop(0)
            # Set it to GREEN.
            lane.turn_green()
            # Remove the lanes from the options that are conflicting.
            options = find_non_conflicting(lane, options)
            # Remove the lane from the queue.
            queue.remove(lane)
