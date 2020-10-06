import random

import config
import simulation
from Models.grid import Grid


def main():
    random.seed(config.RANDOM_SEED)
    grid = Grid(config)

    simulation.run(grid, config.MAX_VEHICLES_PER_STEP)


if __name__ == "__main__":
    main()
