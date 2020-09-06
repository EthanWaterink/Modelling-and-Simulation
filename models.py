from enum import Enum, IntEnum
import random
from config import *


class Turning(IntEnum):
    """The possible turns a car can take"""
    LEFT = 0
    STRAIGHT = 1
    RIGHT = 2


class Direction(IntEnum):
    """The four orthogonal directions"""
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    # returns in what direction a car is going after turning
    def turn(self, turning):
        return (self + 1 + turning) % len(Direction)


class Light(Enum):
    ON = 0
    OFF = 1


class Car(object):
    """Car object"""

    # All cars have the same constant velocity in km/h.
    VELOCITY = 50

    # Because the road length is constant as well, the time it takes to drive to the other side is constant,
    # namely time = 3600 * velocity * distance
    TIME = 3600 * VELOCITY * ROAD_LENGTH

    def __init__(self):
        # TODO: choose from lanes (not all lanes have all Turnings)
        self.turning = random.choice(list(Turning))
        self.destination = None
        self.direction = DEFAULT_DIRECTION

    def __str__(self):
        return "Car[" + str(self.VELOCITY) + " km/h, turning " + str(self.direction) + "]"

    def drive(self):
        print("Driving")
        # wait TIME seconds
        print("Arrived at ", self.destination)


class Intersection(object):
    """Intersection object"""

    def __init__(self, h, w):
        # a maximum of 4 neighbours (one for each direction)
        self.neighbours = [None, None, None, None]
        # in every direction there is a maximum of 3 lanes,
        # depending on the orientation and neighbours of the intersection
        self.lanes = [[None, None, None], [None, None, None], [None, None, None], [None, None, None]]
        # position [h,w] on the grid
        self.h = h
        self.w = w

    def __str__(self):
        return "Intersection[" + str(self.h) + "," + str(self.w) + "]"

    def requiresTrafficLights(self):
        return sum(n is not None for n in self.neighbours) >= 3


class Lane(object):
    """Lane object"""

    def __init__(self, intersection):
        self.intersection = intersection
        self.cars = []  # cars waiting in front of red light (could possibly be a counter?)
