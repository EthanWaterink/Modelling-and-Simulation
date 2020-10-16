import numpy as np

from services import file_service


def step_vehicles(grid):
    """
    Update the vehicles. They can either drive or have to wait.
    """
    finished_vehicles = 0

    # Separate the vehicles into two lists, one for vehicles that can drive, and one for those that have to wait
    can_drive, wait = [], []
    for vehicle in grid.vehicles:
        if not vehicle.is_finished():
            can_drive.append(vehicle) if vehicle.can_drive() else wait.append(vehicle)

    # Update all waiting vehicles
    for vehicle in wait:
        # The vehicle can't drive. It waits one step
        vehicle.steps_waiting += 1

    # Update all vehicles that can drive
    for vehicle in can_drive:
        # Update the time the vehicle is driving.
        vehicle.steps_driving += 1

        # Move the vehicle. If the vehicle reached its destination increase the finished vehicles counter.
        finished_vehicles += vehicle.move_vehicle()

    return finished_vehicles


def step(grid, traffic_light_model):
    """
    Do one step in the simulation
    """
    # Set the states of the traffic lights at all intersections using the traffic light model.
    for intersection in [intersection for row in grid.intersections for intersection in row]:
        traffic_light_model(intersection)

    # Now all GREEN lights are updated, loop over all vehicles and update their states.
    return step_vehicles(grid)


def save_results(vehicles, results_path, traffic_light_model):
    """
    Save the results and write them to a file
    """
    results = {
        'model': traffic_light_model,
        'mean_number_of_steps': np.mean([v.total_steps() for v in vehicles]),
        'mean_number_of_traffic_lights': np.mean([v.number_of_encountered_traffic_lights for v in vehicles]),
        'simulation_score': np.mean([v.steps_waiting / v.number_of_encountered_traffic_lights for v in vehicles])
    }

    file_service.write_results_to_file(results_path + '/results.csv', results)


def run(grid, traffic_light_model):
    """
    Run the simulation
    """
    # Keep track of the steps in which a vehicle finished.
    vehicles_driving = len(grid.vehicles)

    # Loop until all vehicles are finished.
    while vehicles_driving:
        # Move one step forward in time by moving the vehicles. Subtract the number of finished vehicles.
        vehicles_driving -= step(grid, traffic_light_model)
