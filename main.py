from datetime import datetime
import random

import config
import simulation
from services import file_service
from traffic_light_models import get_traffic_light_models
from models.grid import Grid


def main():
    results_file_name = file_service.get_results_path(config.RESULTS_FOLDER_PATH)

    # Multiple grids are generated at random with a random seed set.
    # This makes sure every run the same grids are generated.
    random.seed(config.RANDOM_SEED)

    for random_seed in random.sample(range(1000), config.SIMULATIONS_PER_MODEL):
        random.seed(random_seed)

        # Generate the grid.
        grid = Grid(config)

        # Try all models.
        for model in get_traffic_light_models():
            simulation.run(grid, model, config.MAX_VEHICLES_PER_STEP, results_file_name)


if __name__ == "__main__":
    main()
