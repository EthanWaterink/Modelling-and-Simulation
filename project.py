import random
from enum import Enum, IntEnum

WIDTH = 6
HEIGHT = 5
ROAD_LENGTH = 1 # km


class Turning(IntEnum):
	"""The possible turns a car can take"""
	LEFT = 0
	STRAIGHT = 1
	RIGHT = 2


class Direction(IntEnum):
	"""The four orthogonal directions"""
	NORTH = 0
	EAST = 1
	SOUTH = 2
	WEST = 3

	# returns in what direction a car is going after turning
	def turn(self, turning):
		return (self+1+turning)%len(Direction)


class Ligth(Enum):
	ON = 0
	OFF = 1


class Car(object):
	"""Car object"""

	# all cars have the same constant velocity in km/h
	VELOCITY = 50 
	# and because the road length is constant as well, the time it takes to drive
	# to the other side is constant, namely time = 3600 * velocity * distance
	TIME = 3600 * VELOCITY * ROAD_LENGTH 

	def __init__(self):
		# TODO: choose from lanes (not all lanes have all Turnings)
		self.turning = random.choice(list(Turning))
		self.destination = None

	def __str__(self):
		return "Car[" + str(self.VELOCITY) + " km/h, turning " + str(self.direction) + "]"

	def drive(self):
		print("Driving")
		# wait TIME seconds
		print("Arrived at ", self.destination)


class Intersection(object):
	"""Intersection object"""
	def __init__(self, h, w):
		# a maximum of 4 neighbours (one for each direction)
		self.neighbours = [None, None, None, None]
		# in every direction there is a maximum of 3 lanes, 
		# depending on the orientation and neighbours of the intersection
		self.lanes = [[None,None,None],[None,None,None],[None,None,None],[None,None,None]]
		# position [h,w] on the grid
		self.h = h
		self.w = w

	def __str__(self):
		return "Intersection[" + str(self.h) + "," + str(self.w) + "]"

	def requiresTrafficLights(self):
		return sum(n is not None for n in self.neighbours) >= 3	


class Lane(object):
	"""Lane object"""
	def __init__(self, intersection):
		self.intersection = intersection
		self.cars = [] # cars waiting in front of red light (could possibly be a counter?)


def setupGrid(width, height):
	# initialize the grid and all intersections
	grid = [[Intersection(h, w) for w in range(width)] for h in range(height)]

	# setup neighbour relations
	for h in range(height):
		for w in range(width):
			intersection = grid[h][w]
			# set neighbours
			if h-1 >= 0:     intersection.neighbours[Direction.NORTH] = grid[h-1][w]
			if w+1 < width:  intersection.neighbours[Direction.EAST]  = grid[h][w+1]
			if h+1 < height: intersection.neighbours[Direction.SOUTH] = grid[h+1][w]
			if w-1 >= 0:     intersection.neighbours[Direction.WEST]  = grid[h][w-1]

			# setup lanes
			setupLanes(intersection)

	return grid

def setupLanes(intersection):
	for direction in list(Direction):
		# skip if there is no road in this direction
		if not intersection.neighbours[direction]:
			continue
		
		# determine whether we can make the turn
		for turn in list(Turning):
			if intersection.neighbours[direction.turn(turn)]:
				# add a lane
				lane = Lane(intersection)
				intersection.lanes[direction][turn] = lane;
				# add traffic lights for cross and T-intersections
				if intersection.requiresTrafficLights():
					lane.trafficLight = Ligth.ON

grid = setupGrid(WIDTH, HEIGHT)