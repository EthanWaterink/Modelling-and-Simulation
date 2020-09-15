from enum import Enum, IntEnum
import random
import matplotlib.pyplot as plt

import setup
from config import *


class Turning(IntEnum):
    """The possible turns a vehicle can take"""
    LEFT = 0
    STRAIGHT = 1
    RIGHT = 2


class Direction(IntEnum):
    """The four orthogonal directions"""
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    # Returns in what direction a vehicle is going after turning.
    def turn(self, turning):
        return (self + 1 + turning) % len(Direction)


class Light(Enum):
    ON = 0
    OFF = 1


class Vehicle(object):
    """Vehicle object"""
    direction: Direction

    # All vehicles have the same constant velocity in km/h.
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
        return "Vehicle[" + str(self.VELOCITY) + " km/h, turning " + str(self.direction) + "]"

    def drive(self):
        print("Driving")
        # wait TIME seconds
        print("Arrived at ", self.destination)


class Intersection(object):
    """Intersection object"""

    def __init__(self, y, x):
        # An intersection has a maximum of 4 neighbours (one for each direction).
        self.neighbours = [None, None, None, None]

        # In every direction there is a maximum of 3 lanes, depending on the orientation and neighbours of the
        # intersection.
        self.lanes = [[None, None, None], [None, None, None], [None, None, None], [None, None, None]]

        # Position [y,x] on the grid
        self.y = y
        self.x = x

    def __str__(self):
        return "Intersection[" + str(self.y) + "," + str(self.x) + "]"

    def requiresTrafficLights(self):
        return sum(n is not None for n in self.neighbours) >= 3


class Lane(object):
    """Lane object"""

    def __init__(self, intersection):
        self.intersection = intersection
        self.vehicles = []  # Cars waiting in front of red light (could possibly be a counter?).


class Grid(object):
    def __init__(self):
        self.grid = setup.setup_grid(WIDTH, HEIGHT)

    def plot_grid(self):
        for row in self.grid:
            for intersection in row:
                plt.plot(intersection.x, intersection.y, 'o', color='blue')
                for i in range(0, 4):
                    neighbour = intersection.neighbours[i]
                    if neighbour is not None:
                        plt.arrow(intersection.x, intersection.y, (neighbour.x - intersection.x) / 2,
                                  (neighbour.y - intersection.y) / 2, head_width=.2, head_length=.2, color='grey')
                        plt.plot([intersection.x, neighbour.x], [intersection.y, neighbour.y], '-', color='black')

        plt.show()
