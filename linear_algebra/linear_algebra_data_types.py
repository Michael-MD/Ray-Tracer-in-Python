import numpy as np


mag = np.linalg.norm
dot = np.dot
cross = np.cross
inv = np.linalg.inv
EPSILON = .1

def vector(x,y,z): return np.array([x,y,z,0])

def point(x,y,z): return np.array([x,y,z,1])

def color(x,y,z): return np.array([x,y,z])

black = color(0,0,0)
white = color(1,1,1)

def normalize(v):
	if mag(v) < EPSILON:
		return v
		# raise ZeroDivisionError("Cannot normalizing zero vector.")
	else:
		return v/mag(v)
