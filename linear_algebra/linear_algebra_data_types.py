import numpy as np


mag = np.linalg.norm
dot = np.dot
cross = np.cross
inv = np.linalg.inv
EPSILON = 1e-5

def vector(x,y,z): return np.array([x,y,z,0])

def point(x,y,z): return np.array([x,y,z,1])

def color(x,y,z): return np.array([x,y,z])

def normalize(v):
	if mag(v) < EPSILON:
		raise ZeroDivisionError("Cannot normalizing zero vector.")
	else:
		return v/mag(v)
