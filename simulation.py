import numpy as np

from services import file_service


def run(grid, traffic_light_model):
    """
    Run the simulation on the grid with traffic_light_model.
    """
    # Keep track of the number of vehicles that are driving.
    vehicles_driving = len(grid.vehicles)

    # The current step in the simulation
    step = 0

    # Loop until all vehicles are finished.
    while vehicles_driving:
        # The number of vehicles that finished at this step.
        num_finished = 0

        # Update the states of the traffic lights at all intersections with traffic lights using the traffic
        # light model.
        for intersection in grid.all_intersections_with_traffic_lights():
            # Update the traffic lights once every intersection.traffic_light_length
            if step % intersection.traffic_light_length == 0:
                traffic_light_model.update(intersection)

        # Update all the roads.
        for intersection in [intersection for row in grid.intersections for intersection in row]:
            for road in [road for road in intersection.outgoing_roads.values()]:
                num_finished += road.update()

        # Update all the lanes.
        for intersection in [intersection for row in grid.intersections for intersection in row]:
            for lane in [lane for road in intersection.incoming_roads.values() for lane in road.lanes.values()]:
                if not lane.has_traffic_light or lane.is_green():
                    lane.update_on_green()
                else:
                    lane.update_on_red()

        # Subtract the number of finished vehicles.
        vehicles_driving -= num_finished

        # Increment the step
        step += 1


def simulation_score(vehicles):
    """
    Return the simulation score.
    """
    return np.mean([v.steps_waiting / v.number_of_encountered_traffic_lights for v in vehicles
                    if v.number_of_encountered_traffic_lights != 0])


def mean_number_of_waiting_steps(vehicles):
    """
    Return the mean number of waiting steps.
    """
    return np.mean([v.steps_waiting for v in vehicles])


def mean_number_of_traffic_lights_encountered(vehicles):
    """
    Return the mean number of traffic lights encountered.
    """
    return np.mean([v.number_of_encountered_traffic_lights for v in vehicles])


def mean_number_of_steps(vehicles):
    """
    Return the mean number of total steps.
    """
    return np.mean([v.total_steps() for v in vehicles])


def save_results(vehicles, results_path, traffic_light_model):
    """
    Save the results and write them to a file
    """
    results = {
        'model': traffic_light_model,
        'mean_number_of_steps': mean_number_of_steps(vehicles),
        'mean_number_of_traffic_lights': mean_number_of_traffic_lights_encountered(vehicles),
        'mean_number_of_waiting_steps': mean_number_of_waiting_steps(vehicles),
        'simulation_score': simulation_score(vehicles)
    }

    file_service.write_results_to_file(results_path + '/results.csv', results)
