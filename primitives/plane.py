from sys import path

path.append("../linear_algebra")
path.append("../ray_casting")

from shape import *
from ray_intersection import intersection
from linear_algebra import *
import numpy as np


class plane(shape):
	def local_normal_at(self, object_point):
		return vector(0,1,0)

	def local_intersect(self,r):
		if abs(r.dir[1]) < EPSILON:	# ray parallel to plane
			return np.array([])
		t = -r.origin[1] / r.dir[1]
		return np.array([intersection(t,self)])

	def bounds(self):
		return [ point(-np.inf,0,-np.inf), point(np.inf,0,np.inf) ]