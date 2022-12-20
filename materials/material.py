from sys import path
path.append("../linear_algebra")

from linear_algebra import *
from solid_pattern import solid_pattern

class material:
	def __init__(self):
		self.ambient = .1
		self.diffuse = .9
		self.specular = .9
		self.shininess = 200.
		self.pat = solid_pattern(white)
		self.reflective = 0.0
		self.transparency = 0.0
		self.refractive_index = 1.0

