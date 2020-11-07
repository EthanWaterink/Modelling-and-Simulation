import random
import numpy as np

import config
import simulation
from services import file_service
from models.grid import Grid
from models.traffic_light_models.clock import Clock
from models.traffic_light_models.local_optimum import LocalOptimum
from models.traffic_light_models.first_come_first_serve import FirstComeFirstServe
from models.traffic_light_models.global_optimum import GlobalOptimum
from visualizations import plot


def main():
    results_file_name = file_service.get_results_path(config.RESULTS_FOLDER_PATH)

    # Multiple grids are generated at random with a random seed set.
    # This makes sure every run the same grids are generated.
    random.seed(config.RANDOM_SEED)

    # The
    traffic_loads = np.linspace(config.TRAFFIC_LOAD_START, config.TRAFFIC_LOAD_END, config.TRAFFIC_LOAD_NUM, dtype=int)

    # Initialize the models
    models = [Clock(), FirstComeFirstServe(), LocalOptimum(), GlobalOptimum()]

    # Keep for all
    data = {}
    for model in models:
        data[model] = {
            'score': np.zeros(config.TRAFFIC_LOAD_NUM),
            'waiting_steps': np.zeros(config.TRAFFIC_LOAD_NUM),
            'traffic_lights': np.zeros(config.TRAFFIC_LOAD_NUM)
        }

    # Loop over all num_vehicles
    for idx, num_vehicles in enumerate(traffic_loads):
        print("Traffic load: {} ({}/{} traffic_loads_num)".format(num_vehicles, idx + 1, config.TRAFFIC_LOAD_NUM))

        for _ in range(config.SIMULATIONS_PER_MODEL):
            # Generate the grid.
            grid = Grid(num_vehicles)

            # Try all models.
            for model in models:
                # Setup the model
                model.setup(grid)
                # Run the simulation.
                simulation.run(grid, model)

                # Compute the simulation score and add it
                data[model]['score'][idx] += simulation.simulation_score(grid.vehicles)
                data[model]['waiting_steps'][idx] += simulation.mean_number_of_waiting_steps(grid.vehicles)
                data[model]['traffic_lights'][idx] += simulation.mean_number_of_traffic_lights_encountered(grid.vehicles)
                # Save the results
                simulation.save_results(grid.vehicles, results_file_name, model.__class__.__name__)

                # Reset the grid for the next simulation
                grid.reset()

        # Compute the average simulation score
        for model in models:
            data[model]['score'][idx] /= config.SIMULATIONS_PER_MODEL
            data[model]['waiting_steps'][idx] /= config.SIMULATIONS_PER_MODEL
            data[model]['traffic_lights'][idx] /= config.SIMULATIONS_PER_MODEL

    # Plot the results
    plot.plot_performance_vs_vehicles(data, traffic_loads, config)


if __name__ == "__main__":
    main()
