from sys import path
path.append("../materials")

import numpy as np
from material import *

class shape:
	def __init__(self):
		self.origin = point(0,0,0)
		self.transform = np.eye(4)
		self.mat = material()
		self.parent = None
