from models.light import Light


class Lane(object):
    """
    Lane at the end of a road where vehicles wait for traffic lights (if any)
    """
    def __init__(self, direction, turning, max_vehicles_per_step: int, road):
        # Vehicles wait in a queue
        self.queue = []
        # How many vehicles can drive in one step
        self.max_vehicles_per_step = max_vehicles_per_step

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

    def is_green(self):
        """
        True if the light is green, False otherwise
        """
        return self.traffic_light == Light.GREEN

    def update_on_green(self):
        """
        Update vehicles in this lane given that the light is green
        """
        # Only the first max_vehicles_per_step vehicles can drive at this step
        for vehicle in self.queue[:self.max_vehicles_per_step]:
            vehicle.cross_intersection()
            vehicle.steps_driving += 1
        del self.queue[:self.max_vehicles_per_step]

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
