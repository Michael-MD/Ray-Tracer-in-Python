from pattern import pattern
import numpy as np

class ring_pattern(pattern):
	def __init__(self,a,b):
		self.a = a
		self.b = b
		pattern.__init__(self)
		
	def pattern_at(self, p):
		return self.a if np.floor(np.sqrt(p[0]**2+p[2]**2)) % 2 == 0 else self.b