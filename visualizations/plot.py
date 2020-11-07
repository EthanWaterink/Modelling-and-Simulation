import matplotlib.pyplot as plt


def plot_grid(grid):
    """
    Create a plot of the grid (returns the figure)
    """
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


def plot_performance_vs_vehicles(data, x, config):
    """
    Plot the average performance over multiple runs versus the number of vehicles (returns the figure).
    """
    fig = plt.figure()
    plt.title("Performance of models\n({})".format(config.to_string()))
    plt.xlabel("Number of vehicles")
    plt.ylabel("Average simulation score")

    # Determine the maximum score
    max_score = -1
    # Plot all the models
    for model, values in data.items():
        max_score = max(max_score, max(values['score']))
        plt.plot(x, values['score'], label=model.__class__.__name__)

    # Indicate score regions
    plt.fill_between(
        x, [0], [0.5],
        label='good',
        alpha=0.1,
        color=[(0.5, 1.0, 0.5)]
    )
    plt.fill_between(
        x, [0.5], [1],
        label='average',
        alpha=0.1,
        color=[(0.5, 0.5, 1.0)]
    )
    plt.fill_between(
        x, [1], [max_score],
        label='bad',
        alpha=0.1,
        color=[(1.0, 0.5, 0.5)]
    )

    plt.legend(loc='upper left')
    plt.grid()
    fig.savefig('visualizations/figures/performance_vs_vehicles.png', dpi=300)

    plt.show()

    return fig
