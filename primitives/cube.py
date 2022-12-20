from sys import path

path.append("../linear_algebra")
path.append("../ray_casting")

from shape import *
from ray_intersection import intersection
from linear_algebra import *
import numpy as np

class cube(shape):
	def bounds(self):
		return [ point(-1,-1,-1), point(1,1,1) ]
	

	def check_axis(self, origin,direction):
		tmin_numerator = -1-origin
		tmax_numerator = 1-origin

		if abs(direction) >= EPSILON:
			tmin = tmin_numerator / direction
			tmax = tmax_numerator / direction
		else:
			tmin = tmin_numerator * np.inf
			tmax = tmax_numerator * np.inf

		if tmin > tmax: return tmax,tmin
		else: return tmin, tmax


	def local_intersect(self,r):
		xtmin, xtmax = self.check_axis(r.origin[0], r.direction[0])
		ytmin, ytmax = self.check_axis(r.origin[1], r.direction[1])
		ztmin, ztmax = self.check_axis(r.origin[2], r.direction[2])

		tmin = max(xtmin, ytmin, ztmin)
		tmax = min(xtmax, ytmax, ztmax)

		if tmin>tmax: return []

		return [intersection(tmin, self), intersection(tmax, self)]

	def local_normal_at(self, object_point ):
		maxc = max(abs(object_point[0]), abs(object_point[1]), abs(object_point[2]))
		
		if maxc == abs(object_point[0]):
			return vector(object_point[0], 0, 0)
		elif maxc == abs(object_point[1]):
			return vector(0, object_point[1], 0)

		return vector(0, 0, object_point[2])

