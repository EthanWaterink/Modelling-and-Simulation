import random

import config
import simulation
from traffic_light_models import get_traffic_light_models
from Models.grid import Grid


def main():
    # Multiple grids are generated at random with a random seed set.
    # This makes sure every run the same grids are generated.
    random.seed(config.RANDOM_SEED)

    for random_seed in random.sample(range(1000), config.SIMULATIONS_PER_MODEL):
        random.seed(random_seed)

        # Generate the grid.
        grid = Grid(config)

        # Try all models.
        for model in get_traffic_light_models():
            simulation.run(grid, model, config.MAX_VEHICLES_PER_STEP)


if __name__ == "__main__":
    main()
