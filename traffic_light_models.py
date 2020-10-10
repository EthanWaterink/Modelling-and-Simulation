import random

from Models.direction import get_next_direction
from Models.intersection import Intersection
from Models.light import Light


def get_traffic_light_models():
    return [clock_model]


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
        for lane in [lane for direction in lanes for lane in direction]:
            if lane is not None and lane.has_traffic_light:
                lane.set_traffic_light_state(Light.RED)

        direction = get_next_direction(intersection.current_direction_green)
        intersection.current_direction_green = direction

    # Set all traffic lights at the new direction to green.
    for lane in lanes[direction]:
        if lane is not None:
            lane.set_traffic_light_state(Light.GREEN)

    # Set the traffic light at the right lane at the direction left from the current one to green.
    if (lane := lanes[get_next_direction(direction)][2]) is not None and lane.has_traffic_light:
        lane.set_traffic_light_state(Light.GREEN)
