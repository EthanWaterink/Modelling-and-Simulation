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

    @staticmethod
    def opposite_direction(direction):
        return (direction + 2) % len(Direction)

    @staticmethod
    def next_direction(direction):
        if direction < 3:
            return direction + 1
        else:
            return 0
