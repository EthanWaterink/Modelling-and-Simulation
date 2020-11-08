# Simulation
RANDOM_SEED = 42
TRAFFIC_LOAD_NUM = 20
TRAFFIC_LOAD_START = 10
TRAFFIC_LOAD_END = 3000
SIMULATIONS_PER_MODEL = 100

# Grid
GRID_WIDTH = 10
GRID_HEIGHT = 10

# Road
ROAD_PROBABILITY = .9  # The probability of an intersection being connected to a neighbouring one (one-directional)
ROAD_LENGTH_BASE = 1  # The number of steps it takes to travel a road
ROAD_LENGTH_DIFF = 85*[0] + 10*[+1] + 5*[+2]

# Lane
LANE_PROBABILITY = .9  # The probability of a lane at the end of a road
TRAFFIC_LIGHT_LENGTH = 1  # How many steps a traffic light will be GREEN
FLOW_THROUGH_BASE = 8  # The number of vehicles that can drive in one step when a light turns GREEN
FLOW_THROUGH_DIFF = 5*[+1] + 80*[0] + 10*[-1] + 5*[-2]

# Vehicle
VEHICLE_MIN_ROADS = (GRID_WIDTH+GRID_HEIGHT) // 2
VEHICLE_MAX_ROADS = (GRID_WIDTH+GRID_HEIGHT) * 2

# Results
RESULTS_FOLDER_PATH = './results/'


def to_string():
    return "spm={}, " \
           "w={}, " \
           "h={}, " \
           "r_base={}, " \
           "t={}, " \
           "f_base={}" \
        .format(SIMULATIONS_PER_MODEL, GRID_WIDTH, GRID_HEIGHT, ROAD_LENGTH_BASE, TRAFFIC_LIGHT_LENGTH, FLOW_THROUGH_BASE)
