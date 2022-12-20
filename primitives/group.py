from sys import path

path.append("../linear_algebra")
path.append("../ray_casting")

from shape import *
from ray_intersection import intersection
from linear_algebra import *
import numpy as np
import itertools
from ray import ray


class group(shape):
	def __init__(self):
		shape.__init__(self)
		self.collection = []
		self.pmin = None
		self.pmax = None


	def bounds(self):
		pmin_all = []
		pmax_all = []
		for s in self.collection:
			a = np.transpose(np.array(s.bounds()))[0:3,:]
			cube_ps_object_space = list(itertools.product(*a))
			cube_ps_world_space = []
			# transform points of cube in object space to world space
			for p in cube_ps_object_space:
				a = np.array( point(*p) )
				cube_ps_world_space.append( s.tr @ a )

			# find minimum and maximum of new cube in world space
			cube_ps_world_space = np.array(cube_ps_world_space)
			
			pmin = np.amin(cube_ps_world_space,axis=0)
			pmax = np.amax(cube_ps_world_space,axis=0)

			pmin_all.append(pmin)
			pmax_all.append(pmax)

		# of all the cube points in world space, find the smallest 
		pmin_all = np.array(pmin_all)
		pmax_all = np.array(pmax_all)

		self.pmin = np.array( np.amin(pmin_all,axis=0) )
		self.pmax = np.array( np.amax(pmax_all,axis=0) )

	def add_child(self, s):
		self.collection.append(s)
		s.parent = self


	def check_axis(self, origin,direction, pmina, pmaxa):
		tmin_numerator = pmina-origin
		tmax_numerator = pmaxa-origin

		if abs(direction) >= EPSILON:
			tmin = tmin_numerator / direction
			tmax = tmax_numerator / direction
		else:
			tmin = tmin_numerator * np.inf
			tmax = tmax_numerator * np.inf

		if tmin > tmax: return tmax,tmin
		else: return tmin, tmax


	def AABB_intersect(self,r):
		xtmin, xtmax = self.check_axis(r.origin[0], r.dir[0], self.pmin[0], self.pmax[0])
		ytmin, ytmax = self.check_axis(r.origin[1], r.dir[1], self.pmin[1], self.pmax[1])
		ztmin, ztmax = self.check_axis(r.origin[2], r.dir[2], self.pmin[2], self.pmax[2])

		tmin = max(xtmin, ytmin, ztmin)
		tmax = min(xtmax, ytmax, ztmax)

		if tmin>tmax: return False

		return True



	def local_intersect(self, r):
		if self.pmin is None or self.pmax is None:
			self.bounds()
		
		xs = []

		if not self.AABB_intersect(r):
			return np.array( xs )

		for s in self.collection:
			m = inv(s.tr)
			local_ray = ray(m@r.origin,m@r.dir)
			xs.extend( s.local_intersect(local_ray) )

		return np.sort( np.array( xs ) )