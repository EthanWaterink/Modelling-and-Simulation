from enum import IntEnum


class Direction(IntEnum):
    """The four orthogonal directions"""
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    # Returns in what direction a vehicle is going after turning.
    def turn(self, turning):
        return (self + 1 + turning) % len(Direction)


def get_opposite_direction(direction):
    return (direction + 2) % len(Direction)


def get_next_direction(direction):
    if direction < 3:
        return direction + 1
    else:
        return 0


def get_lane_number(origin_direction, goal_direction):
    if goal_direction - origin_direction == 1 or goal_direction - origin_direction == -3:
        return 0

    if abs(goal_direction - origin_direction) == 2:
        return 1

    if goal_direction - origin_direction == -1 or goal_direction - origin_direction == 3:
        return 2
