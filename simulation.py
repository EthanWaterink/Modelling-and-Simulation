import random

from models import Direction


def determine_green_direction(intersection):
    green_direction = Direction.next_direction(intersection.last_direction_green)
    while intersection.outgoing[green_direction] is None:
        green_direction = Direction.next_direction(green_direction)
    return green_direction


def move_vehicles(grid, max_vehicles_per_step):
    # Loop over all intersections and determine for each intersection the next green light.
    for row in grid.intersections:
        for intersection in row:
            green_direction = determine_green_direction(intersection)

            for vehicle in intersection.vehicles[green_direction][0:max_vehicles_per_step]:
                direction = random.choice([intersection.outgoing.index(lane) for lane in intersection.outgoing if lane])

                # Remove the vehicle from the current intersection and add it to the next.
                # FIXME: the vehicle can drive past multiple intersections in one step because of the order of
                #  intersections.
                intersection.vehicles[green_direction].pop()
                intersection.outgoing[direction].vehicles[Direction.opposite_direction(direction)].append(vehicle)
                vehicle.origin_direction = Direction.opposite_direction(direction)


def run(grid, max_vehicles_per_step):
    for step in range(grid.number_of_steps):
        move_vehicles(grid, max_vehicles_per_step)
        grid.plot_grid(step)
