from pattern import pattern


class checkered_pattern(pattern):
	def __init__(self,a,b):
		self.a = a
		self.b = b
		pattern.__init__(self)
		
	def pattern_at(self, p):
		return self.a if (np.floor(p[0])+np.floor(p[1])+np.floor(p[2])) % 2 == 0 else self.b
