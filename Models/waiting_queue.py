from queue import Queue

from Models.light import Light


class WaitingQueue(object):
    queue = []
    has_traffic_light = False
    traffic_light = Light.RED
