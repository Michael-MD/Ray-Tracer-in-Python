from pattern import pattern

class solid_pattern(pattern):
	def __init__(self,a):
		self.a = a
		pattern.__init__(self)
		
	def pattern_at(self, p):
		return self.a