import models
import random
import config


def setup_grid(width, height):
    # Initialize the grid and all intersections.
    grid = [[models.Intersection(h, w) for w in range(width)] for h in range(height)]

    # Setup neighbour relations.
    for h in range(height):
        for w in range(width):
            intersection = grid[h][w]

            # Set a neighbour based on a probability.
            if h - 1 >= 0 and random.random() <= config.NEIGHBOUR_PROBABILITY:
                intersection.neighbours[models.Direction.NORTH] = grid[h - 1][w]
            if w + 1 < width and random.random() <= config.NEIGHBOUR_PROBABILITY:
                intersection.neighbours[models.Direction.EAST] = grid[h][w + 1]
            if h + 1 < height and random.random() <= config.NEIGHBOUR_PROBABILITY:
                intersection.neighbours[models.Direction.SOUTH] = grid[h + 1][w]
            if w - 1 >= 0 and random.random() <= config.NEIGHBOUR_PROBABILITY:
                intersection.neighbours[models.Direction.WEST] = grid[h][w - 1]

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
