import random
from matplotlib import pyplot as plt
from matplotlib import animation

from models import Direction


def determine_green_direction(intersection):
    green_direction = Direction.next_direction(intersection.last_direction_green)
    while intersection.outgoing[green_direction] is None:
        green_direction = Direction.next_direction(green_direction)
    return green_direction


def move_vehicles(grid, max_vehicles_per_step):
    # Loop over all intersections and determine for each intersection the next green light.
    for row in grid.intersections:
        for intersection in row:
            green_direction = determine_green_direction(intersection)

            for vehicle in intersection.vehicles[green_direction][0:max_vehicles_per_step]:
                direction = random.choice([intersection.outgoing.index(lane) for lane in intersection.outgoing if lane])

                # Remove the vehicle from the current intersection and add it to the next.
                # FIXME: the vehicle can drive past multiple intersections in one step because of the order of
                #  intersections.
                intersection.vehicles[green_direction].pop()
                intersection.outgoing[direction].vehicles[Direction.opposite_direction(direction)].append(vehicle)
                vehicle.origin_direction = Direction.opposite_direction(direction)


def run(grid, max_vehicles_per_step):
    # Plot the grid which will act as the background
    fig = grid.plot_grid()
    # Change the limits of the plot
    plt.xlim([-0.5, grid.width-0.5])
    plt.ylim([-0.5, grid.height])
    # Text for the current time step (centered above the grid)
    time_text = plt.text(
        (grid.width-1)/2.0,
        grid.height-0.5,
        s='step = 0',
        ha='center', va='bottom', fontsize=12
    )

    def animate(i):
        # Update the time step text (i starts at 0, so do +1)
        time_text.set_text('step = %d' % (i+1))

        # Move one step forward in time by moving the vehicles
        move_vehicles(grid, max_vehicles_per_step)

        # Update the text showing the (new) number of cars at the intersections
        num_cars = []
        for row in grid.intersections:
            for intersection in row:
                num_cars.append(plt.text(
                    intersection.x,
                    intersection.y,
                    s=str(intersection.num_cars_waiting()),
                    color="black", backgroundcolor="lightgrey", va="center", ha="center", fontsize=12))

        return num_cars+[time_text]

    # Start the animation
    anim = animation.FuncAnimation(
        fig,
        animate,
        frames=grid.number_of_steps,
        interval=1000,
        blit=True,
        repeat=False
    )
    plt.show()
