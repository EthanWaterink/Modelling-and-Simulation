from models.light import Light


class WaitingQueue(object):
    """
    The WaitingQueue is where vehicles are positioned at an intersection. It is in essence the incoming lane
    with (possibly) a traffic light
    """
    max_vehicles_per_step: int

    def __init__(self, direction, lane_number, max_vehicles_per_step: int):
        self.queue = []
        self.has_traffic_light = False
        self.traffic_light = Light.RED
        self.direction = direction
        self.lane_number = lane_number
        self.max_vehicles_per_step = max_vehicles_per_step

    def __repr__(self):
        return "Lane[{},{}]".format(self.direction, self.lane_number)

    def set_traffic_light_state(self, state: Light):
        """
        Set the state of the traffic light, if applicable
        """
        if self.has_traffic_light:
            self.traffic_light = state

    def can_drive_this_step(self, vehicle):
        """
        Return True if the vehicle can drive this step, which is the case when it is one of the first
        max_vehicles_per_step vehicles in the queue. False otherwise.
        """
        return self.queue.index(vehicle) < self.max_vehicles_per_step
