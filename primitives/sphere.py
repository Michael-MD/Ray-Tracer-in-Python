from sys import path

path.append("../linear_algebra")
path.append("../ray_casting")

from shape import *
from ray_intersection import intersection
from linear_algebra import *
import numpy as np

class sphere(shape):
	def bounds(self):
		return [ point(-1,-1,-1), point(1,1,1) ]

	def local_intersect(self, r):
		sphere_to_ray = r.origin - self.origin
		a = dot(r.dir,r.dir)
		b = 2 * dot(r.dir,sphere_to_ray)
		c = dot(sphere_to_ray,sphere_to_ray) - 1

		delta = b**2 - 4*a*c
		if delta < 0: return np.array([])
		t1 = (-b - np.sqrt(delta)) / (2 * a)
		t2 = (-b + np.sqrt(delta)) / (2 * a)
		return np.array([
							intersection(t1,self),
							intersection(t2,self)
						])

	def local_normal_at(self, object_point):
		return object_point