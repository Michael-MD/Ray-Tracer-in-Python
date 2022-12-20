from sys import path
path.append("../ppm_file")
path.append("../ray_casting")
path.append("../linear_algebra")
path.append("../lights")

from surface_lighting import *
from linear_algebra import *
from ppm_file import *
from cast_ray_to_canvas import *
from ray_intersection import *
from world import *
from group_transform import *


def render(cam, w):
	image = ppmFile(cam.hsize, cam.vsize)
	for y in range( 0, cam.vsize ):
		print(y)
		for x in range( 0, cam.hsize ):
			r = ray_for_pixel(cam, x, y)
			c = color_at(w, r)
			image.write_pixel(x, y, c)
	return image


def is_shadowed(w,p):
	v = w.light.position - p
	distance = mag(v)
	direction = normalize(v)
	r = ray(p,direction)
	intersections = intersect_world(w,r)
	h= hit(intersections)
	if h != None and h.t < distance:
		return True
	else:
		return False


def color_at(w,r,remaining = 5):
	xs = intersect_world(w,r)
	x = hit(xs)
	if x == None: return color(0,0,0)
	comps = prepare_computations(x,r,xs)
	return shade_hit(w,comps,remaining)


class prepare_computations:
	def __init__(self,i, r, xs = []):
		self.t = i.t
		self.object = i.object
		self.p = position_calc(r, self.t)
		self.eyev = -r.dir
		self.normalv = normal_at(self.object, self.p)
		self.reflectv = reflect(r.dir,self.normalv)

		if dot(self.normalv, self.eyev) < 0:
			self.inside = True
			self.normalv = -self.normalv
		else:
			self.inside = False

		self.over_point = self.p+self.normalv*EPSILON
		self.under_point = self.p-self.normalv*EPSILON

		containers = []
		for x in xs:
			if i is x:
				if len(containers) == 0:
					self.n1 = 1.0
				else:
					self.n1 = containers[-1].mat.refractive_index

			if x.object in containers:
				containers.remove(x.object)
			else:
				containers.append(x.object)

			if i is x:
				if len(containers) == 0:
					self.n2 = 1.0
				else:
					self.n2 = containers[-1].mat.refractive_index


def normal_at(s,world_point):
	object_point = world_to_object(s,world_point)
	object_normal = s.local_normal_at(object_point)
	world_normal = normal_to_world(s,object_normal)
	world_normal[-1] = 0
	return normalize(world_normal)


def shade_hit(w,comps, remaining):
	shadowed = is_shadowed(w,comps.over_point)
	surface = lighting(comps.object,w.light,comps.p, comps.eyev, comps.normalv, shadowed)
	reflected = reflected_color( w,comps,remaining )
	refracted = refracted_color( w,comps,remaining )

	m = comps.object.mat
	if m.reflective > 0 and m.transparency > 0:
		reflectance  = schlick(comps)
		c =  surface + reflected*reflectance + refracted*(1-reflectance)
	else:
		c =  surface + reflected + refracted
	return np.minimum( c, color(1,1,1) )
