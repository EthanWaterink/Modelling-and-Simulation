from queue import Queue

from models.light import Light


class WaitingQueue(object):
    def __init__(self, direction, lane_number):
        self.queue = []
        self.has_traffic_light = False
        self.traffic_light = Light.RED
        self.direction = direction
        self.lane_number = lane_number

    def set_traffic_light_state(self, state: Light):
        if self.has_traffic_light:
            self.traffic_light = state
