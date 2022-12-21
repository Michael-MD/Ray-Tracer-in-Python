from sys import path

path.append("../linear_algebra")
path.append("../ray_casting")
path.append("../ray_casting")
path.append("../obj_file")

from shape import *
from ray_intersection import intersection
from linear_algebra import *
import numpy as np
import itertools
from ray import ray
from group import group
import re
from triangle import triangle

class obj_file:
	def __init__(self, filename, fan_triangulation = False):
		self.f = open(filename, "r")
		self.verts = []
		self.faces = []
		self.fan_triangulation = fan_triangulation

		def add_face(v1,v2,v3):
			self.faces.append( [self.verts[ int(v1)-1 ], self.verts[ int(v2)-1 ], self.verts[ int(v3)-1 ]] )


		for x in self.f:
			l = re.split("\s+",x)
			if l[0] == 'v':
				self.verts.append( point( float(l[1]), float(l[2]), float(l[3]) ) )

			if l[0] == 'f':
				v1 = re.split("/",l[1])[0]
				v2 = re.split("/",l[2])[0]
				v3 = re.split("/",l[3])[0]
				v4 = re.split("/",l[4])[0]
				
				add_face(v1,v2,v3)
				if v4 != '':
					add_face(v1,v3,v4)

		self.f.close()

class obj_model(obj_file, group):
	def __init__(self, filename):
		obj_file.__init__(self, filename)
		group.__init__(self)


		for face in self.faces:
			t = triangle( *face )
			t.mat = self.mat
			self.add_child( t )