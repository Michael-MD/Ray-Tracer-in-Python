from sys import path

path.append("../linear_algebra")
path.append("../ray_casting")

from shape import *
from ray_intersection import intersection
from linear_algebra import *
import numpy as np
from double_nabbed_cone import double_nabbed_cone

class cone(double_nabbed_cone):
	def __init__(self):
		double_nabbed_cone.__init__(self)
		self.max = 0
		self.min = -1
		self.isclosed = True
		self.transform = translation(vector(0,.5,0))

	def bounds(self):
		a = double_nabbed_cone.bounds(self)
		return [ t(0,.5,0) @ a[0], t(0,.5,0) @ a[1] ] 

	def __setattr__(self, name, value):
		if name == 'tr':
			double_nabbed_cone.__setattr__(self,name, value@t(0,.5,0))
		else:
			double_nabbed_cone.__setattr__(self,name, value)
