import matplotlib.pyplot as plt

import setup


class Grid(object):
    def __init__(self, config):
        self.width = config.GRID_WIDTH
        self.height = config.GRID_HEIGHT
        self.intersections = setup.setup_intersections(config)
        self.vehicles = setup.setup_vehicles(self, config.MIN_VEHICLES, config.MAX_VEHICLES,
                                             config.VEHICLE_MIN_ROADS, config.VEHICLE_MAX_ROADS)

    # Create a plot of the grid (returns the figure)
    def plot_grid(self):
        fig = plt.figure()
        for row in self.intersections:
            for intersection in row:
                if intersection is None:
                    continue

                # Plot lanes
                for i in range(0, 4):
                    neighbour = intersection.outgoing[i]
                    if neighbour is not None:
                        plt.arrow(intersection.x, intersection.y, (neighbour.x - intersection.x) / 2,
                                  (neighbour.y - intersection.y) / 2, head_width=.2, head_length=.2, color='grey')
                        plt.plot([intersection.x, neighbour.x], [intersection.y, neighbour.y], '-', color='black')

                # Plot number of vehicles
                plt.text(
                    intersection.x,
                    intersection.y,
                    s=str(intersection.num_vehicles_waiting()),
                    color="black", backgroundcolor="lightgrey", va="center", ha="center", fontsize=12
                )

                # Set the title
                plt.title("Simulation street grid with traffic lights")

        return fig
