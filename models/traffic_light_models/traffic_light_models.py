from abc import ABC, abstractmethod

from models.intersection import Intersection
from models.lane import Lane

# The traffic light combinations a.k.a. TLComb
TRAFFIC_LIGHT_COMBINATIONS = [
    # D                   D+L                   D+S                   D+R
    # L     S     R       L      S      R       L     S      R        L      S      R
    [[True, True, True], [False, False, True], [True, False, False], [False, False, True]],  # L, D
    [[True, True, True], [False, False, True], [False, True, True], [False, False, False]],  # S, D
    [[True, True, True], [True, False, True], [False, True, True], [True, True, True]]  # R, D
]


class TrafficLightModel(ABC):
    """
    The base class of traffic light models
    """
    @abstractmethod
    def setup(self, grid):
        """
        Setup the traffic light model.
        """
        return

    @abstractmethod
    def update(self, intersection: Intersection):
        """
        Update the intersection's traffic lights.
        """
        return


def all_traffic_lights_red(intersection):
    """
    Set all traffic lights to RED.
    """
    for road in intersection.incoming_roads.values():
        for lane in road.lanes.values():
            lane.turn_red()


def is_traffic_light_combination_possible(reference_lane, other_lane):
    """
    Returns true if the traffic light combination between reference_lane and lane is possible.
    """
    # The reference lane, which determines the row in TLComb.
    ref_T = reference_lane.turning
    # The direction has to be transformed. The TLComb assumes that the reference direction is at 0, and the
    # other_lane's direction should be relative to that.
    oth_D = other_lane.direction.diff(reference_lane.direction)
    # The other lane
    oth_T = other_lane.turning
    # Check if this combination is possible using the TLComb
    return TRAFFIC_LIGHT_COMBINATIONS[ref_T][oth_D][oth_T]


def find_non_conflicting(reference_lane, lanes: [Lane]):
    """
    Find the lanes the would cause a conflict if they were GREEN simultaneously with reference_lane
    """
    non_conflicting = []
    for other_lane in lanes:
        if is_traffic_light_combination_possible(reference_lane, other_lane):
            non_conflicting .append(other_lane)

    return non_conflicting
