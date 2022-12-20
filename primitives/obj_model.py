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
from obj_file import obj_file
from group import group

class obj_model(obj_file,group):
	def __init__(self, filename):
		objFile.__init__(self,filename)
		group.__init__(self)


		for face in self.faces:
			t = triangle( *face )
			self.add_child( t )