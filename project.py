import random
from enum import IntEnum

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

class Car(object):
	"""Car object"""
	velocity = 50 # all cars have the same velocity

	def __init__(self):
		self.turning = random.choice(list(Turning))

	def __str__(self):
		return "Car[" + str(self.velocity) + " km/h, turning " + str(self.direction) + "]"


class Intersection(object):
	"""Intersection object"""
	def __init__(self, h, w):
		# a maximum of 4 neighbours (one for each direction)
		self.neighbours = [None, None, None, None]
		# in every direction there is a maximum of 3 lanes, 
		# depending on the orientation and neighbours of the intersection
		self.lanes = [None, None, None, None]
		# position [h,w] on the grid
		self.h = h
		self.w = w

	def __str__(self):
		return "Intersection[" + str(self.h) + "," + str(self.w) + "]"



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
	for h in range(height):
		for w in range(width):
			intersection = grid[h][w]
			for direction in list(Direction):
				# skip if there is no road in this direction
				if intersection.neighbours[direction] == None:
					continue

				# TODO: probably better way to implement this:
				# 0 means this lane can be used, -1 if not
				
				# determine whether we can make the turn
				intersection.lanes[direction] = [
					0 if intersection.neighbours[(direction+3)%len(Direction)] else -1,
					0 if intersection.neighbours[(direction+2)%len(Direction)] else -1,
					0 if intersection.neighbours[(direction+1)%len(Direction)] else -1
				]

	return grid


WIDTH = 6
HEIGHT = 5
grid = setupGrid(WIDTH, HEIGHT)