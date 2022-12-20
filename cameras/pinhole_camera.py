import numpy as np

class pinhole_camera:
	def __init__(self,hsize,vsize,fov):
		self.fov = fov
		self.hsize=hsize
		self.vsize=vsize
		self.transform = np.eye(4)
		self.half_view = np.tan( fov/2 )
		self.aspect = hsize/vsize
		if self.aspect >= 1:
			self.half_width = self.half_view
			self.half_height = self.half_view / self.aspect
		else:
			self.half_width = self.half_view * self.aspect
			self.half_height = self.half_view

		self.pixel_size = (self.half_width * 2) / self.hsize