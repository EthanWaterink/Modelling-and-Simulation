import random

import config
from models.light import Light


class Lane(object):
    """
    Lane at the end of a road where vehicles wait for traffic lights (if any)
    """
    def __init__(self, direction, turning, road):
        # Vehicles wait in a queue
        self.queue = []

        # True if this lane has a traffic light
        self.has_traffic_light = False
        # By default, traffic lights are RED
        self.traffic_light = Light.RED

        # The direction at the intersection
        self.direction = direction
        # The turning of the lane
        self.turning = turning
        # The road we go to (after turning at direction)
        self.goes_to_road = road

    def __repr__(self):
        return "Lane[{},{}]".format(self.direction, self.turning)

    def enter(self, vehicle):
        """
        The vehicle enters the lane (and gets in the queue)
        """
        self.queue.append(vehicle)

    def set_traffic_light_state(self, state: Light):
        """
        Set the state of the traffic light, if applicable
        """
        if self.has_traffic_light:
            self.traffic_light = state

    def turn_green(self):
        """
        Set the state of the traffic light to GREEN.
        """
        self.set_traffic_light_state(Light.GREEN)

    def turn_red(self):
        """
        Set the state of the traffic light to RED.
        """
        self.set_traffic_light_state(Light.RED)

    def is_green(self):
        """
        True if the light is green, False otherwise
        """
        return self.traffic_light == Light.GREEN

    def has_vehicles(self):
        """
        True if there is at least one vehicle, False otherwise.
        """
        return len(self.queue) > 0

    def update_on_green(self):
        """
        Update vehicles in this lane given that the light is green.
        """
        # The flow through can differ slightly
        flow_through = config.FLOW_THROUGH_BASE + random.choice(config.FLOW_THROUGH_DIFF)
        # Only the first flow_through vehicles can drive at this step
        for vehicle in self.queue[:flow_through]:
            vehicle.cross_intersection()
            vehicle.steps_driving += 1
        del self.queue[:flow_through]

        # The remaining vehicles have to wait
        for vehicle in self.queue:
            vehicle.steps_waiting += 1

    def update_on_red(self):
        """
        Update vehicles in this lane given that the light is red
        """
        # The vehicles have to wait
        for vehicle in self.queue:
            vehicle.steps_waiting += 1

    def reset(self):
        """
        Reset the lane by removing the vehicles from the queue and turning the light to RED
        """
        del self.queue[:]
        self.traffic_light = Light.RED
