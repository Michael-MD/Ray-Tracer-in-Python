from pattern import pattern


class gradient_pattern(pattern):
	def __init__(self,a,b):
		self.a = a
		self.b = b
		pattern.__init__(self)
		
	def pattern_at(self, p):
		return self.a + (self.b - self.a)*(p[0]-np.floor(p[0]))