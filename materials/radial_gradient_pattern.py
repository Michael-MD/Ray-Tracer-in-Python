from pattern import pattern
import numpy as np


class radial_gradient_pattern(pattern):
	def __init__(self,a,b):
		self.a = a
		self.b = b
		pattern.__init__(self)
		
	def pattern_at(self, p):
		rad = np.sqrt(p[0]**2+p[2]**2) 
		return self.a + (self.b - self.a)*(rad-np.floor(rad))
