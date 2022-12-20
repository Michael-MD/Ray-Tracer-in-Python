from sys import path
path.append("../linear_algebra")
path.append("../ray_casting")

from linear_algebra import *
from ray import *

def ray_for_pixel(cam, px, py):
	xoffset = (px + 0.5) * cam.pixel_size
	yoffset = (py + 0.5) * cam.pixel_size

	world_x = cam.half_width - xoffset
	world_y = cam.half_height - yoffset

	pixel = inv(cam.transform) @ point(world_x, world_y, -1)
	origin = inv(cam.transform) @ point(0, 0, 0)
	direction = normalize(pixel - origin)
	return ray(origin, direction)