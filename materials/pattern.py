from sys import path
path.append("../linear_algebra")
path.append("../render")

import numpy as np
from group_transform import *

class pattern:
	def __init__(self):
		self.transform = np.eye(4)

	def pattern_at(self, p):
		return color(0,0,0)

	def pattern_at_object(self,s,world_point):
		object_point =  world_to_object(s,world_point)
		pattern_point =  inv(self.transform) @ object_point
		return self.pattern_at( pattern_point)