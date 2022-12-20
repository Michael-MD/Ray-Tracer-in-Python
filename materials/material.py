from sys import path
path.append("../linear_algebra")

from linear_algebra import *
from solid_pattern import solid_pattern
from checkered_pattern import checkered_pattern
from gradient_pattern import gradient_pattern
from radial_gradient_pattern import radial_gradient_pattern
from ring_pattern import ring_pattern
from stripe_pattern import stripe_pattern

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

