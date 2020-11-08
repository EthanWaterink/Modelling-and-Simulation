import random
import operator

import config
from models.direction import Direction
from models.intersection import Intersection
from models.turning import Turning
from models.vehicle import Vehicle
from models.traffic_light_models.traffic_light_models import is_traffic_light_combination_possible


def setup_intersections():
    """
    Set up the intersections by adding outgoing and incoming lanes, and traffic lights.
    :return: the intersections
    """

    # The positional differences of the directions (e.g. pos_diff[NORTH] is one up on the y-axis)
    pos_diff = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    ]

    def is_inside(pos):
        """
        Returns True if this position lies on the grid, False otherwise
        """
        return (0 <= pos[0] < config.GRID_WIDTH) and (0 <= pos[1] < config.GRID_HEIGHT)

    def next_pos(pos, direction):
        """
        Returns the position at the direction side of pos
        """
        return tuple(map(operator.add, pos, pos_diff[direction]))

    def get_neighbour(pos, direction):
        """
        Returns the neighbouring intersection if it is inside the grid, None otherwise
        """
        n = next_pos(pos, direction)
        if is_inside(n):
            return intersections[n[0]][n[1]]
        return None

    def setup_roads():
        """
        Set up the roads, defining the neighbour relations.
        """

        def gets_outgoing_road():
            """
            True if the random number is less than or equal to the neighbour probability, False otherwise
            """
            return random.random() <= config.ROAD_PROBABILITY

        def get_neighbour_options(position):
            """
            Returns a dictionary{Direction, Intersection} of possible neighbour intersections, which are those next
            to position that lie on the grid.
            """
            opt = {}
            for D in Direction:
                # If this is a valid neighbour, add it to the options
                if neigh := get_neighbour(position, D):
                    opt[D] = neigh
            return opt

        def initial_roads():
            """
            Setup the initial roads, which are determined by the ROAD_PROBABILITY for every intersection pair.
            """
            for intersection in [intersection for row in intersections for intersection in row]:
                for D in Direction:
                    if (neighbour := get_neighbour(intersection.position(), D)) and gets_outgoing_road():
                        intersection.add_road(neighbour, D)

        def minimum_roads():
            """
            Make sure that every intersection has at least one incoming and one outgoing road.
            """
            for intersection in [intersection for row in intersections for intersection in row]:
                # Check if this intersection has at least one outgoing road
                if len(intersection.outgoing_roads) == 0:
                    options = get_neighbour_options(intersection.position())
                    # Choose an outgoing road
                    direction, destination = random.choice(list(options.items()))
                    # Add it to the intersection
                    intersection.add_road(destination, direction)

                # Check if this intersection has at least one incoming road
                if len(intersection.incoming_roads) == 0:
                    options = get_neighbour_options(intersection.position())
                    # Choose an incoming road
                    direction, destination = random.choice(list(options.items()))
                    # Add it to the intersection (as an outgoing road of the destination intersection)
                    destination.add_road(intersection, direction.opposite())

        def fix_single_roads():
            """
            Make sure that for every incoming road there is an outgoing road (which is not on the same side because
            we do not allow U-turns!). Also make sure that for every outgoing lane there is an incoming lane.
            """
            # Keep track if any intersection was updated
            intersection_updated = False

            for intersection in [intersection for row in intersections for intersection in row]:
                # Check all incoming roads
                for D_inc, road_inc in intersection.incoming_roads.items():
                    # Get the outgoing roads that are on different sides
                    outgoing_roads_on_different_sides = intersection.outgoing_roads.copy()
                    # Remove the side that the incoming road is on (if it is there)
                    if D_inc in outgoing_roads_on_different_sides:
                        outgoing_roads_on_different_sides.pop(D_inc)

                    # Check if there is at least one outgoing road on the different sides
                    if len(outgoing_roads_on_different_sides) == 0:
                        # Get the neighbouring intersections
                        options_outgoing = get_neighbour_options(intersection.position())
                        # Remove the side that the incoming road is on
                        options_outgoing.pop(D_inc)
                        # Choose an intersection
                        direction, destination = random.choice(list(options_outgoing.items()))
                        # Add the outgoing road to the intersection
                        intersection.add_road(destination, direction)

                        intersection_updated = True

                # Check all outgoing roads
                for D_out, road_out in intersection.outgoing_roads.items():
                    # Get the incoming roads that are on different sides
                    incoming_roads_on_different_sides = intersection.incoming_roads.copy()
                    # Remove the side that the outgoing road is on (if it is there)
                    if D_out in incoming_roads_on_different_sides:
                        incoming_roads_on_different_sides.pop(D_out)

                    # Check if there is at least one incoming road on the different sides
                    if len(incoming_roads_on_different_sides) == 0:
                        # Get the neighbouring intersections
                        options_incoming = get_neighbour_options(intersection.position())
                        # Remove the side that the outgoing road is on
                        options_incoming.pop(D_out)
                        # Choose an intersection
                        direction, destination = random.choice(list(options_incoming.items()))
                        # Add the incoming road to the intersection (as an outgoing road of the destination
                        # intersection)
                        destination.add_road(intersection, direction.opposite())

                        intersection_updated = True

            return intersection_updated

        # Setup the initial roads
        initial_roads()
        # Make sure they meet the first requirement
        minimum_roads()
        # Make sure they meet the second requirement
        requires_new_run = fix_single_roads()
        # If an intersection was updated, the second requirement might not be met, so go over the roads again.
        while requires_new_run:
            requires_new_run = fix_single_roads()

    def setup_lanes():
        """
        Set up incoming lanes for each intersection. A lane is added at incoming[D,T] if there is an outgoing lane after
        turning T at direction D.
        """
        def gets_incoming_lane():
            """
            True if the random number is less than or equal to the neighbour probability, False otherwise
            """
            return random.random() <= config.LANE_PROBABILITY

        def initial_lanes():
            """
            Setup the initial lanes, which are determined by the LANE_PROBABILITY for every incoming road.
            """
            for intersection in [intersection for row in intersections for intersection in row]:
                for D, road in intersection.incoming_roads.items():
                    for T in Turning:
                        # Check if there is an outgoing road when turning T from D
                        if D.turn(T) in intersection.outgoing_roads and gets_incoming_lane():
                            road.add_lane(T, intersection.outgoing_roads[D.turn(T)])

        def minimum_per_incoming_road():
            """
            Make sure that every incoming road has at least one lane (so that vehicles can exit the road).
            """
            for intersection in [intersection for row in intersections for intersection in row]:
                for D, road_inc in intersection.incoming_roads.items():
                    # Check if this road has at least one lane
                    if len(road_inc.lanes) == 0:
                        options: [Turning] = []
                        for T in Turning:
                            # If there is a road at D.turn(T) add it to the options
                            if D.turn(T) in intersection.outgoing_roads:
                                options.append(T)

                        # Choose a random lane
                        T_choice = random.choice(options)
                        # Add it to the road
                        road_inc.add_lane(T_choice, intersection.outgoing_roads[D.turn(T_choice)])

        def minimum_per_outgoing_road():
            """
            Make sure that every outgoing road can be reach by at least one lane (so that vehicles can enter the road).
            """
            for intersection in [intersection for row in intersections for intersection in row]:
                for D_out, road_out in intersection.outgoing_roads.items():
                    # Get the incoming lanes
                    incoming_roads_on_different_sides = intersection.incoming_roads.copy()
                    # Remove the side that the incoming road is on (if it is there)
                    if D_out in incoming_roads_on_different_sides:
                        incoming_roads_on_different_sides.pop(D_out)

                    # Keep track if there is at least one lane going to road_out
                    has_at_least_one_lane_going_to_road_out = False

                    # For every incoming road (on different sides) check if there is a lane to road_out
                    for D_inc, road_inc in incoming_roads_on_different_sides.items():
                        # Get the lane that would go to road_out
                        T = D_inc.lane(D_out)
                        # Check if the lane exists
                        if T in road_inc.lanes:
                            has_at_least_one_lane_going_to_road_out = True
                            break

                    # If there is no lane going to road_out, choose random incoming road to add a lane to.
                    if not has_at_least_one_lane_going_to_road_out:
                        # Random incoming road
                        D_inc, road_inc = random.choice(list(incoming_roads_on_different_sides.items()))
                        # Get the lane that would go to road_out
                        T = D_inc.lane(D_out)
                        # Add the lane to the road
                        road_inc.add_lane(T, road_out)

        # Setup the initial lanes
        initial_lanes()
        # Make sure they meet the first requirement
        minimum_per_incoming_road()
        # Make sure they meet the second requirement
        minimum_per_outgoing_road()

    def setup_traffic_lights():
        """
        Set up the traffic lights where necessary. That is, every lane that conflicts with another requires a traffic
        light, lanes with no conflicts do not.
        """
        for intersection in [intersection for row in intersections for intersection in row]:
            for lane_ref in intersection.get_all_lanes():
                # Check if the lanes already has a traffic light (determined by conflicts with another traffic light).
                if not lane_ref.has_traffic_light:
                    for lane_other in intersection.get_all_lanes():
                        # Check if the two lanes conflict
                        if not is_traffic_light_combination_possible(lane_ref, lane_other):
                            intersection.has_traffic_lights = True
                            lane_ref.has_traffic_light = True
                            lane_other.has_traffic_light = True

        # For all intersections that have traffic lights, set the traffic light length
        for intersection in [intersection for row in intersections for intersection in row]:
            if intersection.has_traffic_lights:
                intersection.traffic_light_length = config.TRAFFIC_LIGHT_LENGTH

    # Initialize the grid and all intersections.
    intersections = [[Intersection(x, y) for y in range(config.GRID_HEIGHT)] for x in range(config.GRID_WIDTH)]

    # Set up the outgoing lanes, incoming lanes and traffic lights (in this order!)
    setup_roads()
    setup_lanes()
    setup_traffic_lights()

    return intersections


def setup_vehicles(grid, num_vehicles):
    """
    Set up the vehicles on the grid. The number of vehicles N \\in [min_vehicles,max_ vehicles] and each vehicles drives
    a distance D \\in [min_roads_to_drive, max_roads_to_drive]
    :return: the array of vehicles
    """
    # The list of vehicles.
    vehicles = []

    # Make a random number of vehicles.
    for _ in range(num_vehicles):
        # Get a random intersection.
        x = random.randint(0, config.GRID_WIDTH - 1)
        y = random.randint(0, config.GRID_HEIGHT - 1)
        intersection = grid.intersections[x][y]

        # Determine the number of roads the vehicle has to drive.
        roads_to_drive = random.randint(config.VEHICLE_MIN_ROADS, config.VEHICLE_MAX_ROADS)

        # Choose a lane
        lane = intersection.get_random_lane()

        # Initialize the vehicle and it to the list.
        vehicle = Vehicle(roads_to_drive, intersection.incoming_roads[lane.direction], lane)
        vehicles.append(vehicle)

    return vehicles
