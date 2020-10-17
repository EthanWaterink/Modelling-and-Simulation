import setup


class Grid(object):
    """
    The Grid contains all the (width * height) intersections and all vehicles
    """

    def __init__(self, config):
        self.width = config.GRID_WIDTH
        self.height = config.GRID_HEIGHT
        self.intersections = setup.setup_intersections(config)
        self.vehicles = setup.setup_vehicles(self, config.MIN_VEHICLES, config.MAX_VEHICLES,
                                             config.VEHICLE_MIN_ROADS, config.VEHICLE_MAX_ROADS)
