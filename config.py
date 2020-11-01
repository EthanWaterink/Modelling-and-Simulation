# Simulation
RANDOM_SEED = 42
SIMULATIONS_PER_MODEL = 10

# Grid
GRID_WIDTH = 10
GRID_HEIGHT = 10

# Road
ROAD_PROBABILITY = .9  # The probability of an intersection being connected to a neighbouring one (one-directional)
ROAD_LENGTH = 1  # The number of steps it takes to travel a road

# Lane
LANE_PROBABILITY = .9  # The probability of a lane at the end of a road
MAX_VEHICLES_PER_STEP = 5  # The number of vehicles that can drive in one step when a light turns GREEN
TRAFFIC_LIGHT_LENGTH = 1  # How many steps a traffic light will be GREEN

# Vehicle
VEHICLE_MIN_ROADS = 20
VEHICLE_MAX_ROADS = 25
MIN_VEHICLES = 1500
MAX_VEHICLES = 1500

# Results
RESULTS_FOLDER_PATH = './results/'


