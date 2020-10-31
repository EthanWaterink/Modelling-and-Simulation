import random

import config
import simulation
from services import file_service
from models.grid import Grid
from models.traffic_light_models.clock import Clock
from models.traffic_light_models.local_optimum import LocalOptimum
from models.traffic_light_models.global_optimum import GlobalOptimum


def main():
    results_file_name = file_service.get_results_path(config.RESULTS_FOLDER_PATH)

    # Multiple grids are generated at random with a random seed set.
    # This makes sure every run the same grids are generated.
    random.seed(config.RANDOM_SEED)

    grid_number = 1

    for random_seed in random.sample(range(1000), config.SIMULATIONS_PER_MODEL):
        random.seed(random_seed)

        # Generate the grid.
        print("Grid number", grid_number)
        grid = Grid(config)

        # Try all models.
        for model in [Clock(grid), LocalOptimum(), GlobalOptimum()]:
            print("  running {} model".format(model.__class__.__name__))
            # Run the simulation.
            simulation.run(grid, model)
            # Save the results
            simulation.save_results(grid.vehicles, results_file_name, model.__class__.__name__)
            # Reset the grid for the next simulation
            grid.reset()

        grid_number += 1


if __name__ == "__main__":
    main()
