from enum import Enum, IntEnum
import random
import matplotlib.pyplot as plt

import setup


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

    @staticmethod
    def opposite_direction(direction):
        if direction < 2:
            return direction + 2
        else:
            return direction - 2

    @staticmethod
    def next_direction(direction):
        if direction < 3:
            return direction + 1
        else:
            return 0


class Light(Enum):
    ON = 0
    OFF = 1


class Vehicle(object):
    """Vehicle object"""

    def __init__(self, roads_to_drive, origin_direction):
        self.roads_to_drive = roads_to_drive

        # TODO: This object is not used yet since the origin direction of each vehicle can also be retrieved from the
        #  intersection the vehicle currently stands. If it will be used nowhere, this object can be removed.
        self.origin_direction = origin_direction


class Intersection(object):
    """Intersection object"""

    def __init__(self, y, x, default_last_direction_green):
        # An intersection has a maximum of 4 neighbours (one for each direction).
        self.incoming = [None, None, None, None]
        self.outgoing = [None, None, None, None]

        # Position [y,x] on the grid
        self.y = y
        self.x = x

        self.vehicles = [[], [], [], []]
        self.last_direction_green: Direction = default_last_direction_green

    def __str__(self):
        return "Intersection[" + str(self.y) + "," + str(self.x) + "]"

    def requires_traffic_lights(self):
        return sum(n is not None for n in self.incoming) >= 3

    def set_last_direction_green(self):
        self.last_direction_green = random.choice([i for i in self.outgoing if i is not None])


class Grid(object):
    def __init__(self, config):
        self.width = config.GRID_WIDTH
        self.height = config.GRID_HEIGHT
        self.intersections = setup.setup_intersections(config)
        self.number_of_steps = setup.setup_vehicles(self, config.MIN_VEHICLES, config.MAX_VEHICLES,
                                                    config.VEHICLE_MIN_ROADS, config.VEHICLE_MAX_ROADS)

    def plot_grid(self, step):
        for row in self.intersections:
            for intersection in row:
                if intersection is None:
                    continue

                # Plot lanes
                for i in range(0, 4):
                    neighbour = intersection.outgoing[i]
                    if neighbour is not None:
                        plt.arrow(intersection.x, intersection.y, (neighbour.x - intersection.x) / 2,
                                  (neighbour.y - intersection.y) / 2, head_width=.2, head_length=.2, color='grey')
                        plt.plot([intersection.x, neighbour.x], [intersection.y, neighbour.y], '-', color='black')

                # Plot number of vehicles
                plt.text(intersection.x, intersection.y,
                         str(sum([len(vehicles) for vehicles in intersection.vehicles])), color="red",
                         backgroundcolor="grey", va="center", ha="center")

                plt.title("Step " + str(step))

        plt.show()
