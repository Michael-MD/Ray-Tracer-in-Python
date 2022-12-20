from sys import path

path.append("../linear_algebra")
path.append("../ray_casting")

from shape import *
from ray_intersection import intersection
from linear_algebra import *
import numpy as np
from ray_intersection import position_calc


class double_nabbed_cone(shape):
	def __init__(self):
		shape.__init__(self)
		self.min = -np.inf
		self.max = np.inf
		self.isclosed = False


	def bounds(self):
		a = max(abs(self.min),abs(self.max))
		return [ point(-a,self.min,-a), point(a,self.max,a) ]

	def check_cap(self,r, t):
		i = position_calc(r,t)
		x,y,z,_ = i
		return (x**2+z**2) <= abs(y)

	def intersect_caps(self,r, xs = []):
		if not self.isclosed:
			return xs
		t = (self.min - r.origin[1]) / r.direction[1]
		if self.check_cap(r, t):
			xs.append(intersection(t, self))

		t = (self.max - r.origin[1]) / r.direction[1]
		if self.check_cap(r, t):
			xs.append(intersection(t, self))

		return xs


	def local_intersect(self, r):
		d = r.direction
		o = r.origin

		a = d[0]**2 - d[1]**2+d[2]**2
		b = 2*o[0]*d[0] - 2*o[1]*d[1] + 2*o[2]*d[2]

		if abs(a) < EPSILON and abs(b) < EPSILON:
			return self.intersect_caps(r)

		c = o[0]**2 - o[1]**2 + o[2]**2

		if (abs(a) < EPSILON and abs(b) > EPSILON):
			t = -c/(2*b)
			xs = [intersection(t,self)]
			return self.intersect_caps(r,xs)

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
		x,_,z,_ = p
		dist = x**2+z**2

		if dist < 1 and p[1] >= self.max - EPSILON:
			return vector(0,1,0)
		elif dist < 1 and p[1] <= self.min + EPSILON:
			return vector(0,-1,0)
		else:
			y= np.sqrt(dist)
			if p[1]>0:
				y = -y
			return vector(x,y,z)
