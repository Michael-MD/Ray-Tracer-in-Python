from sys import path

path.append("../linear_algebra")
path.append("../ray_casting")

from shape import *
from ray_intersection import intersection
from linear_algebra import *
import numpy as np
from ray_intersection import position_calc


class cylinder(shape):
	def __init__(self):
		shape.__init__(self)
		self.min = -np.inf
		self.max = np.inf
		self.isclosed = False

	def bounds(self):
		return [ point(-1,self.min,-1), point(1,self.max,1) ]

	def check_cap(self,r, t):
		i = position_calc(r,t)
		x = i[0]
		z = i[2]
		return (x**2+z**2) <= 1

	def intersect_caps(self,r, xs = []):
		if not self.isclosed or abs(r.direction[1]) < EPSILON:
			return xs

		t = (self.min - r.origin[1]) / r.direction[1]
		if self.check_cap(r, t):
			xs.append(intersection(t, self))

		t = (self.max - r.origin[1]) / r.direction[1]
		if self.check_cap(r, t):
			xs.append(intersection(t, self))

		return xs


	def local_intersect(self, r):
		a = r.direction[0]**2 + r.direction[2]**2

		if abs(a) < EPSILON:
			return self.intersect_caps(r)

		b = 2 * r.origin[0] * r.direction[0] + 2 * r.origin[2] * r.direction[2]
		c = r.origin[0]**2 + r.origin[2]**2 - 1
		disc = b**2 - 4 * a * c
		if disc < 0: return []

		intersections = []

		t0 = (-b - np.sqrt(disc)) / (2 * a)
		t1 = (-b + np.sqrt(disc)) / (2 * a)

		y0 = position_calc(r,t0)[1]
		if y0 < self.max and y0 > self.min:
			intersections.append( intersection(t0, self) )

		y1 = position_calc(r,t1)[1]
		if y1 < self.max and y1 > self.min:
			intersections.append( intersection(t1, self) )


		return self.intersect_caps(r, intersections)

	def local_normal_at(self, p):
		x = p[0]
		z = p[2]
		dist = x**2+z**2

		if dist < 1 and p[1] >= self.max - EPSILON:
			return vector(0,1,0)
		elif dist < 1 and p[1] <= self.min + EPSILON:
			return vector(0,-1,0)
		else:
			return vector(p[0], 0, p[2])