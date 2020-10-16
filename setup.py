import random

from models.direction import Direction, get_opposite_direction
from models.intersection import Intersection
from models.vehicle import Vehicle


def add_incoming_lanes(grid, width, height):
    for y in range(height):
        for x in range(width):
            for outgoing_direction in range(4):
                if (goal_intersection := grid[y][x].outgoing[outgoing_direction]) is not None:
                    goal_intersection.add_incoming_lane(get_opposite_direction(outgoing_direction))


def add_outgoing_lanes(origin_intersection, goal_intersection, direction):
    origin_intersection.add_outgoing_lane(goal_intersection, direction)


def add_traffic_lights(grid, width, height):
    for y in range(height):
        for x in range(width):
            if grid[y][x] is None:
                continue

            # If there are incoming lanes coming from more than 1 direction, traffic lights have to be added.
            if sum([1 if len([lane for lane in grid[y][x].incoming[incoming_direction] if lane]) > 1 else 0 for
                    incoming_direction in range(4)]) > 1:
                grid[y][x].add_traffic_lights()


def setup_intersections(config):
    # Initialize the grid and all intersections.
    grid = [[Intersection(y, x, config.DEFAULT_LAST_DIRECTION_GREEN) for x in range(config.GRID_WIDTH)] for y in
            range(config.GRID_HEIGHT)]

    # Setup neighbour relations.
    # TODO: Make sure every intersection has at least one incoming and one outgoing lane.
    for y in range(config.GRID_HEIGHT):
        for x in range(config.GRID_WIDTH):
            intersection = grid[y][x]

            # Set a neighbour based on a probability.
            if y - 1 >= 0 and random.random() <= config.NEIGHBOUR_PROBABILITY:
                add_outgoing_lanes(intersection, grid[y - 1][x], Direction.SOUTH)
            if x + 1 < config.GRID_WIDTH and random.random() <= config.NEIGHBOUR_PROBABILITY:
                add_outgoing_lanes(intersection, grid[y][x + 1], Direction.EAST)
            if y + 1 < config.GRID_HEIGHT and random.random() <= config.NEIGHBOUR_PROBABILITY:
                add_outgoing_lanes(intersection, grid[y + 1][x], Direction.NORTH)
            if x - 1 >= 0 and random.random() <= config.NEIGHBOUR_PROBABILITY:
                add_outgoing_lanes(intersection, grid[y][x - 1], Direction.WEST)

    add_incoming_lanes(grid, config.GRID_WIDTH, config.GRID_HEIGHT)
    add_traffic_lights(grid, config.GRID_WIDTH, config.GRID_HEIGHT)

    return grid


def setup_vehicles(grid, min_vehicles, max_vehicles, min_roads_to_drive, max_roads_to_drive):
    # Make a random number of vehicles. Save the number of roads the vehicle with the longest journey has to drive.
    max_roads = 0
    vehicles = []

    for _ in range(random.randint(min_vehicles, max_vehicles)):
        # Get a random intersection.
        x = random.randint(0, grid.width - 1)
        y = random.randint(0, grid.height - 1)

        # Determine the number of roads the vehicle has to drive and add the vehicle to the list of the intersection.
        roads_to_drive = random.randint(min_roads_to_drive, max_roads_to_drive)
        intersection = grid.intersections[y][x]
        (origin_direction, lane_number) = intersection.get_random_waiting_queue()

        vehicle = Vehicle(roads_to_drive, origin_direction, intersection)
        intersection.incoming[origin_direction][lane_number].queue.append(vehicle)
        vehicle.waiting_queue = intersection.incoming[origin_direction][lane_number]
        vehicles.append(vehicle)

        # If there is a new maximum of roads a vehicle has to drive, save it.
        if roads_to_drive > max_roads:
            max_roads = roads_to_drive

    return vehicles
