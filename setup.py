import models
import random
import config


def get_entrance_coordinate(side, possible_indices):
    random.shuffle(possible_indices[side])
    return possible_indices[side].pop()


def setup_grid(width, height):
    random.seed(config.RANDOM_SEED)

    # Initialize the grid and all intersections. Add margins at each side for the entrances/exits.
    grid = [[models.Intersection(y, x) for x in range(width + 2)] for y in range(height + 2)]

    # Setup neighbour relations.
    for y in range(1, height+1):
        for x in range(1, width+1):
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

    # Create entrances/exits.
    possible_indices = [[*range(1, width+1)], [*range(1, height+1)], [*range(1, width+1)], [*range(1, height+1)]]
    for side in random.sample(range(4), config.OFF_GRID_CONNECTIONS):
        print("side: %d" % side)

        if side == 0:  # North
            x = get_entrance_coordinate(side, possible_indices)
            y = height + 1
            grid[y][x].neighbours[models.Direction.SOUTH] = grid[y-1][x]
            grid[y-1][x].neighbours[models.Direction.NORTH] = grid[y][x]
        elif side == 1:  # East
            y = get_entrance_coordinate(side, possible_indices)
            x = width + 1
            grid[y][x].neighbours[models.Direction.WEST] = grid[y][x-1]
            grid[y][x-1].neighbours[models.Direction.EAST] = grid[y][x]
        elif side == 2:  # South
            x = get_entrance_coordinate(side, possible_indices)
            y = 0
            grid[y][x].neighbours[models.Direction.NORTH] = grid[y-1][x]
            grid[y-1][x].neighbours[models.Direction.SOUTH] = grid[y][x]
        else:  # West
            y = get_entrance_coordinate(side, possible_indices)
            x = 0
            grid[y][x].neighbours[models.Direction.EAST] = grid[y][x+1]
            grid[y][x+1].neighbours[models.Direction.WEST] = grid[y][x]

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
