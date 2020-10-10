import random

from models.direction import get_next_direction, get_opposite_direction
from models.intersection import Intersection
from models.light import Light
from models.waiting_queue import WaitingQueue


def get_traffic_light_models():
    return [clock_model, local_optimum_with_priority_model]


def clock_model(intersection: Intersection):
    lanes = intersection.incoming

    # If this method is called for the first time, turn on all lights at a random direction.
    # We know that this method is called for the first time when the current green direction is not set.
    if intersection.current_direction_green is None:
        # Choose a random direction.
        direction = random.randint(0, 3)
        intersection.current_direction_green = direction

    # If this method is not called for the first time, all lights are set to red and the new direction is set.
    else:
        all_traffic_lights_red(lanes)
        direction = get_next_direction(intersection.current_direction_green)
        intersection.current_direction_green = direction

    # Set all traffic lights at the new direction to green.
    for lane in lanes[direction]:
        if lane is not None:
            lane.set_traffic_light_state(Light.GREEN)

    # Set the traffic light at the right lane at the direction left from the current one to green.
    if (lane := lanes[get_next_direction(direction)][2]) is not None and lane.has_traffic_light:
        lane.set_traffic_light_state(Light.GREEN)


def local_optimum_with_priority_model(intersection: Intersection):
    def get_highest_priority_lane(lanes: [WaitingQueue]):
        max_lane = None
        max_queue_length = -1

        for lane in lanes:
            if len(lane.queue) > max_queue_length:
                max_lane = lane
                max_queue_length = len(lane.queue)

        return max_lane

    def find_conflicts(lanes: [WaitingQueue], reference_lane):
        conflicts = []
        for lane in lanes:
            if not is_traffic_light_combination_possible(reference_lane, lane):
                conflicts.append(lane)

        return conflicts

    lanes_per_direction: [[WaitingQueue]] = intersection.incoming

    # All traffic lights are set to red.
    all_traffic_lights_red(lanes_per_direction)
    options: [WaitingQueue] = [lane for lanes in lanes_per_direction for lane in lanes if lane]

    while len(options) > 0:
        highest_priority_lane = get_highest_priority_lane(options)
        options.remove(highest_priority_lane)
        for lane in find_conflicts(options, highest_priority_lane):
            if lane is not None:
                options.remove(lane)
        highest_priority_lane.set_traffic_light_state(Light.GREEN)


def all_traffic_lights_red(lanes):
    for lane in [lane for direction in lanes for lane in direction]:
        if lane is not None and lane.has_traffic_light:
            lane.set_traffic_light_state(Light.RED)


def is_traffic_light_combination_possible(reference_lane, lane):
    def next_direction_can_be_green(base_lane, left_lane):
        # The traffic light at lane which is at the left of the base lane can be turned to green if the left lane is for
        # making a right turn, or when the left lane is making a right turn and the base lane is making a left turn.
        return left_lane.lane_number == 2 or (base_lane.lane_number == 2 and left_lane.lane_number == 0)

    # When coming from the same direction, both traffic lights can always be green.
    if reference_lane.direction == lane.direction:
        return True

    # When the directions of the two lanes only differ one, we can use the inner function.
    if get_next_direction(reference_lane.direction) == lane.direction:
        return next_direction_can_be_green(reference_lane, lane)

    if reference_lane.direction == get_next_direction(lane.direction):
        return next_direction_can_be_green(lane, reference_lane)

    # If the lanes are from the opposite directions, they only cannot drive if only one of them are turning left.
    if reference_lane.direction == get_opposite_direction(lane.direction):
        return reference_lane.lane_number == lane.lane_number or reference_lane.lane_number != 0 or\
               lane.lane_number != 0
