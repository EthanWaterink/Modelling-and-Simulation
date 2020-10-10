from queue import Queue

from Models.light import Light


class WaitingQueue(object):
    def __init__(self):
        self.queue = []
        self.has_traffic_light = False
        self.traffic_light = Light.RED

    def set_traffic_light_state(self, state: Light):
        if self.has_traffic_light:
            self.traffic_light = state
