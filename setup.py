import models
import random
import config


def setup_grid(width, height):
    random.seed(config.RANDOM_SEED)

    # Initialize the grid and all intersections. Add margins at each side for the entrances/exits.
    grid = [[models.Intersection(y, x) for x in range(width)] for y in range(height)]

    # Setup neighbour relations.
    for y in range(height):
        for x in range(width):
            intersection = grid[y][x]

            # Set a neighbour based on a probability.
            if y - 1 > 0 and random.random() <= config.NEIGHBOUR_PROBABILITY:
                intersection.neighbours[models.Direction.SOUTH] = grid[y - 1][x]
            if x + 1 < width and random.random() <= config.NEIGHBOUR_PROBABILITY:
                intersection.neighbours[models.Direction.EAST] = grid[y][x + 1]
            if y + 1 < height and random.random() <= config.NEIGHBOUR_PROBABILITY:
                intersection.neighbours[models.Direction.NORTH] = grid[y + 1][x]
            if x - 1 > 0 and random.random() <= config.NEIGHBOUR_PROBABILITY:
                intersection.neighbours[models.Direction.WEST] = grid[y][x - 1]

            # Setup lanes
            setup_lanes(intersection)

    return grid


def setup_lanes(intersection):
    for direction in list(models.Direction):
        # Skip if there is no road in this direction.
        if not intersection.neighbours[direction]:
            continue

        # Determine whether we can make the turn.
        for turn in list(models.Turning):
            if intersection.neighbours[direction.turn(turn)]:
                # Add a lane.
                lane = models.Lane(intersection)
                intersection.lanes[direction][turn] = lane

                # Add traffic lights for cross and T-intersections.
                if intersection.requiresTrafficLights():
                    lane.trafficLight = models.Light.ON


def setup_vehicles(grid):
    for vehicle_id in range(random.randint(3, config.WIDTH * config.HEIGHT)):
        x = random.randint(0, config.WIDTH - 1)
        y = random.randint(0, config.HEIGHT - 1)

        while grid[y][x] is None:
            x = random.randint(0, config.WIDTH)
            y = random.randint(0, config.HEIGHT)

        grid[y][x].vehicles.append(models.Vehicle(vehicle_id))

