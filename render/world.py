from sys import path
path.append("../linear_algebra")
path.append("ray_casting")

import numpy as np
from linear_algebra import *
from ray import ray

class world:
	def __init__(self):
		self.objects = []
		self.light = None


def intersect_world(w, r):
	intersections = []
	for s in w.objects:
		m = inv(s.transform)
		local_ray = ray(m@r.origin,m@r.dir) 
		intersections.extend( s.local_intersect(local_ray) )
	return np.sort(intersections)
