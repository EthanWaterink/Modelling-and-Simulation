import matplotlib.pyplot as plt

from models.direction import Direction


# Create a plot of the grid (returns the figure)
def plot_grid(grid):
    fig = plt.figure()
    for intersection in [intersection for row in grid.intersections for intersection in row]:
        # Plot lanes
        for road in intersection.outgoing_roads.values():
            neighbour = road.destination
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

    plt.show()

    return fig
