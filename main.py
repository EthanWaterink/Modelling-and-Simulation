import random

import config
from models import Grid


def main():
    random.seed(config.RANDOM_SEED)
    grid = Grid(config.GRID_WIDTH, config.GRID_HEIGHT, config.NEIGHBOUR_PROBABILITY)
    grid.plot_grid()


if __name__ == "__main__":
    main()
