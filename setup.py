import random

import models


def add_lanes(origin_intersection, goal_intersection, direction):
    origin_intersection.outgoing[direction] = goal_intersection
    goal_intersection.incoming[models.Direction.opposite_direction(direction)] = origin_intersection


def setup_intersections(config):
    # Initialize the grid and all intersections.
    grid = [[models.Intersection(y, x, config.DEFAULT_LAST_DIRECTION_GREEN) for x in range(config.GRID_WIDTH)] for y in
            range(config.GRID_HEIGHT)]

    # Setup neighbour relations.
    # TODO: Make sure every intersection has at least one incoming and one outgoing lane.
    for y in range(config.GRID_HEIGHT):
        for x in range(config.GRID_WIDTH):
            intersection = grid[y][x]

            # Set a neighbour based on a probability.
            if y - 1 >= 0 and random.random() <= config.NEIGHBOUR_PROBABILITY:
                add_lanes(intersection, grid[y - 1][x], models.Direction.SOUTH)
            if x + 1 < config.GRID_WIDTH and random.random() <= config.NEIGHBOUR_PROBABILITY:
                add_lanes(intersection, grid[y][x + 1], models.Direction.EAST)
            if y + 1 < config.GRID_HEIGHT and random.random() <= config.NEIGHBOUR_PROBABILITY:
                add_lanes(intersection, grid[y + 1][x], models.Direction.NORTH)
            if x - 1 >= 0 and random.random() <= config.NEIGHBOUR_PROBABILITY:
                add_lanes(intersection, grid[y][x - 1], models.Direction.WEST)

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
        origin_direction = random.choice(
            [intersection.incoming.index(neighbour) for neighbour in intersection.incoming if neighbour])

        vehicle = models.Vehicle(roads_to_drive, origin_direction, intersection)
        intersection.vehicles[origin_direction].append(vehicle)
        vehicles.append(vehicle)

        # If there is a new maximum of roads a vehicle has to drive, save it.
        if roads_to_drive > max_roads:
            max_roads = roads_to_drive

    return max_roads, vehicles
