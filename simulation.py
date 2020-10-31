import numpy as np

from services import file_service


def step(grid, traffic_light_model):
    """
    Do one step in the simulation by updating the traffic lights, roads and lanes.
    """
    # The number of vehicles that finished at this step.
    num_finished = 0

    # Set the states of the traffic lights at all intersections using the traffic light model.
    for intersection in [intersection for row in grid.intersections for intersection in row]:
        if intersection.has_traffic_lights:
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

    return num_finished


def run(grid, traffic_light_model):
    """
    Run the simulation
    """
    # Keep track of the number of vehicles that are driving.
    vehicles_driving = len(grid.vehicles)

    # Loop until all vehicles are finished.
    while vehicles_driving:
        # Move one step forward in time by moving the vehicles. Subtract the number of finished vehicles.
        vehicles_driving -= step(grid, traffic_light_model)


def save_results(vehicles, results_path, traffic_light_model):
    """
    Save the results and write them to a file
    """
    results = {
        'model': traffic_light_model,
        'mean_number_of_steps': np.mean([v.total_steps() for v in vehicles]),
        'mean_number_of_traffic_lights': np.mean([v.number_of_encountered_traffic_lights for v in vehicles]),
        'mean_number_of_waiting_steps': np.mean([v.steps_waiting for v in vehicles]),
        'simulation_score': np.mean([v.steps_waiting / v.number_of_encountered_traffic_lights for v in vehicles
                                     if v.number_of_encountered_traffic_lights != 0])
    }

    file_service.write_results_to_file(results_path + '/results.csv', results)
