import random
from enum import Enum, IntEnum
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
        return (direction + 2) % len(Direction)

    @staticmethod
    def next_direction(direction):
        if direction < 3:
            return direction + 1
        else:
            return 0


class Light(Enum):
    ON = 0
    OFF = 1


class Intersection(object):
    """Intersection object"""
    def __init__(self, y, x, default_direction_green: Direction):
        # An intersection has a maximum of 4 neighbours (one for each direction).
        self.incoming = [None, None, None, None]
        self.outgoing = [None, None, None, None]

        # Position [y,x] on the grid
        self.y = y
        self.x = x

        self.vehicles = [[], [], [], []]
        self.current_direction_green = default_direction_green

    def __str__(self):
        return "Intersection[" + str(self.y) + "," + str(self.x) + "]"

    def requires_traffic_lights(self):
        return sum([1 for lane in self.incoming if lane]) >= 3

    def num_cars_waiting(self):
        return sum([len(vehicles) for vehicles in self.vehicles])


class Vehicle(object):
    """Vehicle object"""
    last_location: Intersection

    def __init__(self, roads_to_drive, origin_direction, location: Intersection):
        self.roads_to_drive = roads_to_drive
        self.origin_direction = origin_direction
        self.current_location = location
        self.steps_driving = 0

    def get_next_direction(self):
        possible_directions = [self.current_location.outgoing.index(lane) for lane in self.current_location.outgoing if lane]

        # If there are more possible directions than one, don't choose the direction the vehicle came from.
        if len(possible_directions) > 1:
            possible_directions.remove(self.origin_direction)

        return random.choice(
            [self.current_location.outgoing.index(lane) for lane in self.current_location.outgoing if lane])


class Grid(object):
    # TODO: remove this variable after the simulation can stop when there are no vehicles left.
    number_of_steps = 25

    def __init__(self, config):
        self.width = config.GRID_WIDTH
        self.height = config.GRID_HEIGHT
        self.intersections = setup.setup_intersections(config)
        self.vehicles = setup.setup_vehicles(self, config.MIN_VEHICLES, config.MAX_VEHICLES,
                                             config.VEHICLE_MIN_ROADS, config.VEHICLE_MAX_ROADS)

    # Create a plot of the grid (returns the figure)
    def plot_grid(self):
        fig = plt.figure()
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
                plt.text(
                    intersection.x,
                    intersection.y,
                    s=str(intersection.num_cars_waiting()),
                    color="black", backgroundcolor="lightgrey", va="center", ha="center", fontsize=12
                )

                # Set the title
                plt.title("Simulation street grid with traffic lights")

        return fig
