import random

from models.direction import Direction
from models.intersection import Intersection
from models.turning import Turning
from models.vehicle import Vehicle


def setup_incoming_lanes(intersections, config):
    """
    Set up incoming lanes for each intersection. A lane is added at incoming[D,T] if there is an outgoing lane after
    turning T at direction D.
    """
    for intersection in [intersection for row in intersections for intersection in row]:
        for (D, T) in [(D, T) for D in Direction for T in Turning]:
            if intersection.outgoing[D.turn(T)] is not None:
                intersection.add_incoming_lanes(D, T, config.MAX_VEHICLES_PER_STEP)


def setup_outgoing_lanes(intersections, config):
    """
    Set up the outgoing lanes, defining the neighbour relations.
    """
    def gets_neighbour():
        """
        True if the random number is less than or equal to the neighbour probability, False otherwise
        """
        return random.random() <= config.NEIGHBOUR_PROBABILITY

    for y in range(config.GRID_HEIGHT):
        for x in range(config.GRID_WIDTH):
            intersection = intersections[y][x]

            # Set a neighbour based on a probability.
            if y - 1 >= 0 and gets_neighbour():
                intersection.add_outgoing_lane(intersections[y - 1][x], Direction.NORTH)
            if x + 1 < config.GRID_WIDTH and gets_neighbour():
                intersection.add_outgoing_lane(intersections[y][x + 1], Direction.EAST)
            if y + 1 < config.GRID_HEIGHT and gets_neighbour():
                intersection.add_outgoing_lane(intersections[y + 1][x], Direction.SOUTH)
            if x - 1 >= 0 and gets_neighbour():
                intersection.add_outgoing_lane(intersections[y][x - 1], Direction.WEST)


def setup_traffic_lights(intersections):
    """
    Set up the traffic lights where necessary.
    """
    for intersection in [intersection for row in intersections for intersection in row]:
        if intersection.required_traffic_lights():
            intersection.add_traffic_lights()


def setup_intersections(config):
    """
    Set up the intersections by adding outgoing and incoming lanes, and traffic lights.
    :return: the intersections
    """
    # Initialize the grid and all intersections.
    intersections = [[Intersection(y, x) for x in range(config.GRID_WIDTH)] for y in range(config.GRID_HEIGHT)]

    # Set up the outgoing lanes, incoming lanes and traffic lights (in this order!)
    # TODO: Make sure every intersection has at least one incoming and one outgoing lane.
    setup_outgoing_lanes(intersections, config)
    setup_incoming_lanes(intersections, config)
    setup_traffic_lights(intersections)

    return intersections


def setup_vehicles(grid, min_vehicles, max_vehicles, min_roads_to_drive, max_roads_to_drive):
    """
    Set up the vehicles on the grid. The number of vehicles N \\in [min_vehicles,max_ vehicles] and each vehicles drives
    a distance D \\in [min_roads_to_drive, max_roads_to_drive]
    :return: the array of vehicles
    """
    vehicles = []

    # Make a random number of vehicles.
    for _ in range(random.randint(min_vehicles, max_vehicles)):
        # Get a random intersection.
        x = random.randint(0, grid.width - 1)
        y = random.randint(0, grid.height - 1)
        intersection = grid.intersections[y][x]

        # Determine the number of roads the vehicle has to drive.
        roads_to_drive = random.randint(min_roads_to_drive, max_roads_to_drive)

        # Get a random waiting queue.
        (origin_direction, origin_turning) = intersection.get_random_waiting_queue()

        # Initialize the vehicles.
        vehicle = Vehicle(roads_to_drive, origin_direction, intersection)

        # Add the vehicle to the list of the intersection.
        intersection.incoming[origin_direction][origin_turning].queue.append(vehicle)
        vehicle.waiting_queue = intersection.incoming[origin_direction][origin_turning]

        vehicles.append(vehicle)

    return vehicles
