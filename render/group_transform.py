from sys import path
path.append("../linear_algebra")

from linear_algebra import *
import numpy as np


def world_to_object(s,p, op = np.eye(4)):
	if s == None: return inv(op) @ p
	return world_to_object(s.parent, p, s.transform @ op )


def normal_to_world(s, normalv):
	normalv = np.transpose(inv(s.transform)) @ normalv
	normalv[3] = 0
	normalv = normalize(normalv)
	if s.parent != None:
		normalv = normal_to_world(s.parent, normalv)
	
	return normalv