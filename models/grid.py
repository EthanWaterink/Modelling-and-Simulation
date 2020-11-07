import config
import setup


class Grid(object):
    """
    The Grid contains all the (width * height) intersections and all vehicles
    """

    def __init__(self, num_vehicles):
        self.intersections = setup.setup_intersections()
        self.vehicles = setup.setup_vehicles(self, num_vehicles)
        self.traffic_light_length = config.TRAFFIC_LIGHT_LENGTH

    def all_intersections_with_traffic_lights(self):
        """
        Returns a list with all intersections that have traffic lights.
        """
        intersections_with_traffic_lights = []
        for intersection in [intersection for row in self.intersections for intersection in row]:
            if intersection.has_traffic_lights:
                intersections_with_traffic_lights.append(intersection)
        return intersections_with_traffic_lights

    def reset(self):
        """
        Reset the grid (by resetting all the roads, lanes and vehicles)
        """
        for intersection in [intersection for row in self.intersections for intersection in row]:
            for road in intersection.outgoing_roads.values():
                for lane in road.lanes.values():
                    lane.reset()
                road.reset()

        for vehicle in self.vehicles:
            vehicle.reset()
