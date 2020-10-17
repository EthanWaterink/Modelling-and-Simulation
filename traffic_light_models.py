import random

from models.direction import Direction
from models.intersection import Intersection
from models.light import Light
from models.turning import Turning
from models.waiting_queue import WaitingQueue

# The traffic light combinations a.k.a. TLComb
TRAFFIC_LIGHT_COMBINATIONS = [
    # D                   D+L                   D+S                   D+R
    # L     S     R       L      S      R       L     S      R        L      S      R
    [[True, True, True], [False, False, True], [True, False, False], [False, False, True]],  # L, D
    [[True, True, True], [False, False, True], [False, True, True], [False, False, False]],  # S, D
    [[True, True, True], [True, False, True], [False, True, True], [True, True, True]]       # R, D
]


def get_traffic_light_models():
    """
    Return a list of all the traffic light models
    """
    return [clock_model, local_optimum_with_priority_model]


def clock_model(intersection: Intersection):
    """
    The clock model
    """
    lanes = intersection.incoming

    # If this method is called for the first time, turn on all lights at a random direction.
    # We know that this method is called for the first time when the current GREEN direction is not set.
    if intersection.current_direction_green is None:
        # Choose a random direction.
        direction = random.choice(list(Direction))
        intersection.current_direction_green = direction
        return

    # Set all lights to RED and the new direction is set.
    all_traffic_lights_red(lanes)
    direction = intersection.current_direction_green.next()
    intersection.current_direction_green = direction

    # Set all traffic lights at the new direction to GREEN.
    for lane in lanes[direction]:
        if is_valid(lane):
            lane.set_traffic_light_state(Light.GREEN)

    # Set the traffic light at the right lane at the direction left from the current one to GREEN.
    if is_valid(lane := lanes[direction.next()][Turning.RIGHT]):
        lane.set_traffic_light_state(Light.GREEN)


def local_optimum_with_priority_model(intersection: Intersection):
    """
    The local optimum model with priority.
    """
    def get_highest_priority_lane(lanes: [WaitingQueue]):
        """
        Return the lane with the highest priority, which is the one with the most vehicles waiting
        """
        max_lane = None
        max_queue_length = -1

        for lane in lanes:
            if len(lane.queue) > max_queue_length:
                max_lane = lane
                max_queue_length = len(lane.queue)

        return max_lane

    def find_conflicts(lanes: [WaitingQueue], reference_lane):
        """
        Find the lanes the would cause a conflict if they were GREEN simultaneously with reference_lane
        """
        conflicts = []
        for lane in lanes:
            if not is_traffic_light_combination_possible(reference_lane, lane):
                conflicts.append(lane)

        return conflicts

    lanes_per_direction: [[WaitingQueue]] = intersection.incoming

    # All traffic lights are set to RED.
    all_traffic_lights_red(lanes_per_direction)
    # Initialize the options list, which contains the lanes whose traffic lights can be set the GREEN
    options: [WaitingQueue] = [lane for lanes in lanes_per_direction for lane in lanes if is_valid(lane)]

    # Loop while there are still options. Note that the options list will contain at most 4 lanes because for each
    # direction there is only one outgoing lane
    while len(options) > 0:
        # Find the lane with the highest priority
        highest_priority_lane = get_highest_priority_lane(options)
        # Remove it from the options list, since it will be set to GREEN and is no longer an option
        options.remove(highest_priority_lane)
        # Remove all the conflicting lanes
        for lane in find_conflicts(options, highest_priority_lane):
            options.remove(lane)
        # Set the highest priority lane to GREEN
        highest_priority_lane.set_traffic_light_state(Light.GREEN)


def is_valid(lane):
    """
    Returns true if the lane is not None and if it has a traffic light, False otherwise
    """
    return lane is not None and lane.has_traffic_light


def all_traffic_lights_red(lanes):
    """
    Set all traffic lights to RED.
    """
    for lane in [lane for direction in lanes for lane in direction]:
        if is_valid(lane):
            lane.set_traffic_light_state(Light.RED)


def is_traffic_light_combination_possible(reference_lane, other_lane):
    """
    Returns true if the traffic light combination between reference_lane and lane is possible.
    """
    # The reference lane, which determines the row in TLComb.
    ref_T = reference_lane.lane_number
    # The direction has to be transformed. The TLComb assumes that the reference direction is at 0, and the
    # other_lane's direction should be relative to that.
    oth_D = other_lane.direction.diff(reference_lane.direction)
    # The other lane
    oth_T = other_lane.lane_number
    # Check if this combination is possible using the TLComb
    return TRAFFIC_LIGHT_COMBINATIONS[ref_T][oth_D][oth_T]
