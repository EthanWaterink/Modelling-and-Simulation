import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import copy

from Models.direction import Direction


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
    finished_cars = 0

    for vehicle in grid.vehicles:
        if vehicle.roads_to_drive == 0:
            continue

        # Update the time the vehicle is driving.
        vehicle.steps_driving += 1

        current_intersection = vehicle.current_location

        # If the traffic light the vehicle is waiting in front of is not green, nothing will change for this vehicle.
        if vehicle.origin_direction != current_intersection.current_direction_green:
            continue

        # Choose the next direction for the vehicle.
        direction = vehicle.get_next_direction()
        next_location = current_intersection.outgoing[direction]

        # If the current vehicle is too far to the back of the queue, the vehicle will not move.
        if current_intersection.vehicles[vehicle.origin_direction].index(vehicle) >= max_vehicles_per_step:
            continue

        # Remove the vehicle from the current intersection and add it to the next.
        current_intersection.vehicles[current_intersection.current_direction_green].remove(vehicle)
        next_location.vehicles[Direction.opposite_direction(direction)].append(vehicle)

        # Update the location in the vehicle model.
        vehicle.last_location = vehicle.current_location
        vehicle.current_location = next_location
        vehicle.origin_direction = Direction.opposite_direction(direction)

        # Update the number of roads the vehicle still has to drive.
        vehicle.roads_to_drive -= 1
        if vehicle.roads_to_drive == 0:
            finished_cars += 1

    return finished_cars


def get_statistics(finished_cars):
    print("Mean number of steps to destination:", round(np.mean(finished_cars), 2))


# Animation of the simulation (for each step)
def simulation_animation(grid_states):
    # Plot the grid which will act as the background
    fig = grid_states[0].plot_grid()
    # Change the limits of the plot
    plt.xlim([-0.5, grid_states[0].width - 0.5])
    plt.ylim([-0.5, grid_states[0].height])
    # Text for the current time step (centered above the grid)
    time_text = plt.text(
        (grid_states[0].width - 1) / 2.0,
        grid_states[0].height - 0.5,
        s='step = 0',
        ha='center', va='bottom', fontsize=12
    )

    def animate(i):
        # Update the time step text (i starts at 0, so do +1)
        time_text.set_text('step = %d' % (i + 1))

        # Update the text showing the (new) number of cars at the intersections at the current time step
        num_cars = []
        for row in grid_states[i].intersections:
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
        frames=len(grid_states),
        interval=500,
        blit=True,
        repeat=False
    )

    # Save the animation in a GIF file
    anim.save('animation.gif')


# Run the simulation
def run(grid, max_vehicles_per_step):
    finished_cars = 0
    # Store the grid states, starting with the initial grid
    grid_states = [copy.deepcopy(grid)]
    # Loop until all cars are finished
    while finished_cars < len(grid.vehicles):
        # Move one step forward in time by moving the vehicles
        number_of_finished_cars = move_vehicles(grid, max_vehicles_per_step)
        finished_cars += number_of_finished_cars

        # Store the current state of the grid
        grid_states.append(copy.deepcopy(grid))

    simulation_animation(grid_states)
    get_statistics(finished_cars)
