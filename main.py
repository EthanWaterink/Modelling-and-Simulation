import random

import config
import simulation
from models import Grid


def main():
    random.seed(config.RANDOM_SEED)
    grid = Grid(config)
    grid.plot_grid(-1)

    simulation.run(grid, config.MAX_VEHICLES_PER_STEP)


if __name__ == "__main__":
    main()
