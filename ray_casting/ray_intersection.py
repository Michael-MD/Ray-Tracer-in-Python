class intersection:
	def __init__(self, t, object):
		self.t = t
		self.object = object

	def __gt__(self, i): return True if self.t > i.t else False
	def __lt__(self, i): return True if self.t < i.t else False
	def __ge__(self, i): return True if self.t >= i.t else False
	def __le__(self, i): return True if self.t <= i.t else False


def position_calc(r, t): return r.origin + r.dir*t

def hit(xs):	# hit assumes xs is ordered
	for x in xs:
		if x.t >= 0:
			return x
	
	return
