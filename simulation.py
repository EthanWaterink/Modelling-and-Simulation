import random

from matplotlib import animation
from matplotlib import pyplot as plt

from models import Direction


def determine_green_direction(intersection):
    green_direction = Direction.next_direction(intersection.current_direction_green)
    while intersection.outgoing[green_direction] is None:
        green_direction = Direction.next_direction(green_direction)
    return green_direction


def move_vehicles(grid, max_vehicles_per_step):
    # Loop over all intersections and determine for each intersection the next green light.
    for row in grid.intersections:
        for intersection in row:
            green_direction = determine_green_direction(intersection)
            intersection.current_direction_green = green_direction

    # Now all green lights are updated, loop over all vehicles and update their states.
    for vehicle in grid.vehicles:
        current_intersection = vehicle.current_location

        # If the traffic light the vehicle is waiting in front of is not green, nothing will change for this vehicle.
        if vehicle.origin_direction != current_intersection.current_direction_green:
            continue

        # Choose the next direction for the vehicle.
        direction = random.choice(
            [current_intersection.outgoing.index(lane) for lane in current_intersection.outgoing if lane])
        next_location = current_intersection.outgoing[direction]

        # Remove the vehicle from the current intersection and add it to the next.
        # TODO: add max number of vehicles which can pass in one step.
        current_intersection.vehicles[current_intersection.current_direction_green].pop()
        next_location.vehicles[Direction.opposite_direction(direction)].append(vehicle)

        # Update the location in the vehicle model.
        vehicle.last_location = vehicle.current_location
        vehicle.current_location = next_location
        vehicle.origin_direction = Direction.opposite_direction(direction)


def run(grid, max_vehicles_per_step):
    # Plot the grid which will act as the background
    fig = grid.plot_grid()
    # Change the limits of the plot
    plt.xlim([-0.5, grid.width - 0.5])
    plt.ylim([-0.5, grid.height])
    # Text for the current time step (centered above the grid)
    time_text = plt.text(
        (grid.width - 1) / 2.0,
        grid.height - 0.5,
        s='step = 0',
        ha='center', va='bottom', fontsize=12
    )

    def animate(i):
        # Update the time step text (i starts at 0, so do +1)
        time_text.set_text('step = %d' % (i + 1))

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

        return num_cars + [time_text]

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
