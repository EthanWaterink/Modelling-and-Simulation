import copy

import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt

from models.direction import get_next_direction
from models.light import Light
from services import file_service


def set_green_direction(intersection):
    if not intersection.has_traffic_lights:
        return None

    green_direction = get_next_direction(intersection.current_direction_green)
    intersection.current_direction_green = green_direction

    for incoming_direction in range(4):
        for lane_number in range(3):
            if intersection.incoming[incoming_direction][lane_number] is None:
                continue

            new_state = Light.GREEN if incoming_direction == green_direction else Light.RED
            intersection.incoming[incoming_direction][lane_number].set_traffic_light_state(new_state)


def move_vehicles(grid, max_vehicles_per_step):
    finished_vehicles = 0

    for vehicle in grid.vehicles:
        if vehicle.roads_to_drive == 0:
            continue

        # Update the time the vehicle is driving.
        vehicle.steps_driving += 1

        if not vehicle.can_drive(max_vehicles_per_step):
            vehicle.waiting_steps += 1
            continue

        # Move the vehicle. If the vehicle reached its destination increase the finished vehicles counter.
        finished_vehicles += vehicle.move_vehicle()

    return finished_vehicles


def step(grid, traffic_light_model, max_vehicles_per_step):
    # Set the states of the traffic lights at all intersections using the traffic light model.
    for intersection in [intersection for row in grid.intersections for intersection in row]:
        traffic_light_model(intersection)

    # Now all green lights are updated, loop over all vehicles and update their states.
    return move_vehicles(grid, max_vehicles_per_step)


def save_results(finished_vehicles, vehicles, results_path, traffic_light_model):
    results = {
        'model': traffic_light_model,
        'mean_number_of_steps': np.mean(finished_vehicles),
        'mean_number_of_traffic_lights': np.mean([v.number_of_encountered_traffic_lights for v in vehicles]),
        'simulation_score': np.mean([v.waiting_steps / v.number_of_encountered_traffic_lights for v in vehicles])
    }

    file_service.write_results_to_file(results_path + '/results.csv', results)


# Animation of the simulation (for each step)
def simulation_animation(grid_states, results_path):
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
        ha='center',
        va='bottom',
        fontsize=12
    )

    def animate(i):
        # Update the time step text (i starts at 0, so do +1)
        time_text.set_text('step = %d' % (i + 1))

        # Update the text showing the (new) number of vehicles at the intersections at the current time step
        num_vehicles = []
        for row in grid_states[i].intersections:
            for intersection in row:
                num_vehicles.append(plt.text(
                    intersection.x,
                    intersection.y,
                    s=str(intersection.num_vehicles_waiting()),
                    color="black", backgroundcolor="lightgrey", va="center", ha="center", fontsize=12))

        return num_vehicles + [time_text]

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
    anim.save(results_path + '/animation.gif')


# Run the simulation
def run(grid, traffic_light_model, max_vehicles_per_step, results_path):
    # Keep track of the steps in which a vehicle finished.
    finished_vehicles = []

    # Store the grid states, starting with the initial grid
    # grid_states = [copy.deepcopy(grid)]

    # Loop until all vehicles are finished
    time_stamp = 0
    while len(finished_vehicles) < len(grid.vehicles):
        time_stamp += 1

        # Move one step forward in time by moving the vehicles. If n vehicles finished this step, add n times the
        # current time stamp to finished_vehicles.
        if (finished_vehicles_in_step := step(grid, traffic_light_model, max_vehicles_per_step)) > 0:
            finished_vehicles.extend(finished_vehicles_in_step * [time_stamp])

        # Store the current state of the grid
        # grid_states.append(copy.deepcopy(grid))

    # simulation_animation(grid_states, results_path)
    save_results(finished_vehicles, grid.vehicles, results_path, traffic_light_model.__name__)
