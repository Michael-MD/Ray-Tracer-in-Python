from sys import path

path.append("../linear_algebra")
path.append("../ray_casting")

from shape import *
from ray_intersection import intersection
from linear_algebra import *
import numpy as np
import itertools
from ray import ray


class triangle(shape):
	def __init__(self,p1,p2,p3):
		shape.__init__(self)
		self.p1 = p1
		self.p2 = p2
		self.p3 = p3
		self.e1 = p2-p1
		self.e2 = p3-p1
		self.normalv = normalize( vector( *np.cross(self.e2[0:3],self.e1[0:3]) ) )

	def bounds(self):
		a = np.array([
			self.p1,
			self.p2,
			self.p3,
			])
		return [ np.amin( a, axis=0 ), np.amax( a, axis=0 ) ]

	def local_normal_at(self,p):
		return self.normalv

	def local_intersect(self,r):
		dir_cross_e2 = vector( *np.cross(r.dir[0:3], self.e2[0:3]) )
		det = np.dot(self.e1, dir_cross_e2)
		if abs(det) < EPSILON:
			return [] 

		f = 1.0 / det
		p1_to_origin = r.origin - self.p1
		u = f * dot(p1_to_origin, dir_cross_e2)
		if u < 0 or u > 1:
			return []

		origin_cross_e1 = vector( *np.cross(p1_to_origin[0:3], self.e1[0:3]) )
		v = f * np.dot(r.dir, origin_cross_e1)
		if v < 0 or (u + v) > 1:
			return [] 


		t = f * np.dot(self.e2, origin_cross_e1)
		return [ intersection(t, self) ]