from enum import IntEnum

from models.turning import Turning


class Direction(IntEnum):
    """
    The four orthogonal directions
    """
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def turn(self, turning: Turning):
        """
        Returns in what direction a vehicle is going after turning.
        """
        return Direction((self + 1 + turning) % len(Direction))

    def opposite(self):
        """
        Return the direction that is opposite to itself
        """
        return Direction((self + 2) % len(Direction))

    def next(self):
        """
        Return the direction that is left of direction (clock-wise)
        """
        return Direction((self + 1) % len(Direction))

    def lane(self, goal_direction):
        """
        Return the lane that goes to goal_direction
        """
        return Turning((goal_direction - self) % len(Turning))

    def diff(self, other):
        """
        Return the difference between the other direction and itself
        """
        return Direction((other - self) % len(Direction))
